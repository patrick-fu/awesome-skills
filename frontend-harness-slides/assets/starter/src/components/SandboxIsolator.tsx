import { useEffect, useRef, type ReactNode, type CSSProperties } from 'react';

type Props = {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
  /** 额外要放行的 key（KeyboardEvent.key），默认空 */
  allowKeys?: string[];
};

// 被 SlideDeck 导航捕获、需要在可编辑上下文中屏蔽的 keys
const NAV_KEYS = new Set([
  ' ', 'Spacebar', 'Enter',
  'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
  'Home', 'End', 'PageUp', 'PageDown', 'Backspace',
  'h', 'j', 'k', 'l', // 类 vim
]);
// 功能键永远放行
const ALWAYS_PASS_KEYS = new Set([
  'Escape', 'Tab',
  'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
  'Shift','Control','Alt','Meta','CapsLock','ContextMenu',
]);

function isEditable(el: EventTarget | null): boolean {
  if (!(el instanceof HTMLElement)) return false;
  // 递归祖先：<span> 放在 contenteditable 里也要识别
  let cur: HTMLElement | null = el;
  while (cur) {
    const tag = cur.tagName;
    if (tag === 'TEXTAREA') return true;
    if (tag === 'SELECT') return true;
    if (tag === 'INPUT') {
      const type = (cur as HTMLInputElement).type;
      // button/checkbox/radio/hidden/range/file/color/submit/reset/image 这些不需要挡
      if (!['button','checkbox','radio','hidden','range','file','color','submit','reset','image'].includes(type)) {
        return true;
      }
      break; // input 是非编辑类型，不继续向上查（避免 contenteditable 外的 span 里套的 input）
    }
    if (cur.isContentEditable) return true;
    cur = cur.parentElement;
  }
  return false;
}

function isInteractive(el: EventTarget | null): boolean {
  if (!(el instanceof HTMLElement)) return false;
  if (el.closest('button, a[href], [role="button"], [role="link"], [role="tab"], summary, label')) return true;
  return false;
}

/**
 * 内部组件（如 React 交互 demo、代码编辑器、可编辑原型）的事件沙箱。
 * 在捕获阶段吞掉会与 SlideDeck 全局键盘/滚动导航冲突的事件，
 * 确保嵌入组件的交互体验与在独立页面中完全一致。
 *
 * 修正：原版本用 React 合成事件 stopPropagation，对 window-level capture 监听器无效。
 * 改为原生 addEventListener(capture: true) + stopImmediatePropagation。
 * // P0-3 FIXED: SandboxIsolator rewritten with native capture listeners
 */
export default function SandboxIsolator({ children, className, style, allowKeys }: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = ref.current;
    if (!root) return;

    const onKeyDownCapture = (e: KeyboardEvent) => {
      if (ALWAYS_PASS_KEYS.has(e.key)) return;
      if (allowKeys?.includes(e.key)) return;

      const target = e.target;
      const inEditable = isEditable(target);
      const inInteractive = isInteractive(target);

      if (inEditable) {
        // 可编辑元素内：所有导航键全吞，不要触发翻页
        if (NAV_KEYS.has(e.key)) {
          e.stopImmediatePropagation();
          // 注意：不要 preventDefault，让文本编辑继续工作
        }
      } else if (inInteractive) {
        // 按钮/链接内：Enter/Space 会触发点击，也不要让它同时翻页
        if (e.key === ' ' || e.key === 'Spacebar' || e.key === 'Enter') {
          e.stopImmediatePropagation();
        }
      }
    };

    const onKeyUpCapture = (e: KeyboardEvent) => {
      if (ALWAYS_PASS_KEYS.has(e.key)) return;
      if ((isEditable(e.target) && NAV_KEYS.has(e.key)) ||
          (isInteractive(e.target) && (e.key === ' ' || e.key === 'Spacebar' || e.key === 'Enter'))) {
        e.stopImmediatePropagation();
      }
    };

    // Wheel：如果 wheel 发生在 root 内，就吞掉（防止冒泡到外层触发页面级滚动/翻页）。
    // 内部滚动仍然自然发生（不 preventDefault），只是 stopImmediatePropagation 不让外层再处理。
    const onWheelCapture = (e: WheelEvent) => {
      e.stopImmediatePropagation();
      // 不 preventDefault，让内部滚动自然发生
    };

    // 指针事件：防止拖拽时被 stage 误判
    const onPointerCapture = (e: PointerEvent) => {
      if (e.target !== root) {
        // 拖拽在子元素上发生时，不冒泡到 stage
        e.stopPropagation();
      }
    };

    const onContextMenuCapture = (e: Event) => {
      e.stopPropagation();
    };

    // 捕获阶段注册（true）是关键：先于 SlideDeck 的 window-level 监听器执行
    root.addEventListener('keydown', onKeyDownCapture, true);
    root.addEventListener('keyup', onKeyUpCapture, true);
    root.addEventListener('wheel', onWheelCapture, true);
    root.addEventListener('pointerdown', onPointerCapture, true);
    root.addEventListener('contextmenu', onContextMenuCapture, true);

    return () => {
      root.removeEventListener('keydown', onKeyDownCapture, true);
      root.removeEventListener('keyup', onKeyUpCapture, true);
      root.removeEventListener('wheel', onWheelCapture, true);
      root.removeEventListener('pointerdown', onPointerCapture, true);
      root.removeEventListener('contextmenu', onContextMenuCapture, true);
    };
  }, [allowKeys]);

  return (
    <div
      ref={ref}
      className={className ?? 'w-full h-full'}
      style={{ ...style, overscrollBehavior: 'contain', isolation: 'isolate' }}
      data-sandbox
    >
      {children}
    </div>
  );
}

export { SandboxIsolator };
