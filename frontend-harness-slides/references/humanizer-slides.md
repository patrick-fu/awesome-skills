# humanizer mode — slide copy that sounds human

When the user asks for humanizer (`speak-like-human: true`), strip corporate hype and mechanical AI symmetry from on-slide text and speaker notes. Replace abstract slogans with concrete, conversational, first-person language.

(Examples below are deliberately in Chinese — they demonstrate what human-voiced Chinese slide copy looks like.)

## Contrastive examples

| Scenario | ❌ AI-slop / corporate | ✅ humanizer |
| :--- | :--- | :--- |
| Login overhaul | "通过重构鉴权管线，我们对底层会话生命周期提供了全链路的安全闭环保障，赋能高弹性的登录持久化体验。" | "登录态过期时，要先保住用户正在编辑的内容。别直接跳转踢人，保留现场，让用户刷新完还能回来继续写。" |
| Introducing the harness | "建设高密度的测试 Harness 承接底层执行质量，闭环收敛技术债务，从而最大化地释放开发提效产能。" | "没有测试的 Loop 只是自动试错。Harness 就像地基，地基稳了，改东西才不怕改坏别的，你才敢放手让 Agent 自己跑。" |
| Context overload | "针对长程任务导致的会话高熵饱和及上下文拥堵痛点，我们设计了物理级别会话隔离的编排机制。" | "任务变长之后，上下文足迹会直接压垮智商。要解决这个拥堵，要么把任务拆出去走编排，要么在主线上把日志压缩熔炼。一个往外拆，一个往里压。" |

## Formatting rules

- **No slogans on screen** — except the title and closing slides, don't put high-sounding marketing lines on a slide. Keep on-slide text to keywords, tags, concrete metrics, or one direct takeaway.
- **First-person practitioner voice** — in speaker notes and explanations, talk from experience ("我试过这个，结果不行，因为……") instead of stating assumptions as universal law.
- **Concrete over abstract** — prefer "保住正在编辑的内容" to "保障体验"; prefer a number or a thing you can point at over an -ization noun.
