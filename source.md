---
tags:
  - project-note
  - task
  - note-draft
---
## 概要

- 現在使用しているAI関連サービスの確認
- 及びその理由

## 使用サービス

### サブスクリプションしているもの

#### Google AI プレミアムプラン

https://gemini.google/advanced/?hl=ja
月額2900円
##### 理由

DeepReserachに回数制限がなく、調査も（実際に自分で試せていないですが）ChatGPTほどではないかもしれないですがしっかり行ってくれる印象
自分の使い方として他の作業と並行して色々な種類のDeepReserachをする事が多い(=回数が多い)ので非常に助かっています

Geminiは他のGoogleエコシステムとの連携が強いと感じます
DeepResearch -> Googleドキュメント -> NotebookLM
などのフローが行え、逆に他Googleサービスからも使用できます
Geminiのコンテキストウィンドウの大きさもその為ではないかと
全体としてみるととてもまとまっている印象
サブスクリプションはまだ試用期間ですが、DeepResearchの回数制限もありこのまま使用し続けると思います

昔からですが、各種サービスを無料/安価で提供しているGoogle先生に感謝を

#### Cursorエディタ Proプラン

https://www.cursor.com/ja
月額20ドル
##### 理由

個人的にプログラムが日常なので開発用としてCursorを使用
Geminiが検索、資料方面を担当してCursorは実作業担当の構えになっています
~~財布が許せばDevinやManusも試したい~~

Cursor限定ではないですがClaude3.7 Sonnet(Thinking)の安定感と頭の良さに驚いています
現状最も安定して作業を行ってくれる印象
エージェントモードは固定しているぐらいですが、使いすぎるとdefaultにしてくれと注意されたり
defaultは作業負荷を見て適宜振り分けてくれるようなのですが、やっぱりClaude3.7固定の方が安定しているので悩ましい所

Cursorエージェントだけで大体書いてくれたのが下記リポジトリです。何かの参考になれば
Gitリポジトリヒートマップ作成
https://github.com/seless-yuu/RepositoryHeatmap


### その他に使用しているAIサービス

#### ChatGPT

主にo3-miniの推論モードを使用
Geminiがちょっと答えてくれない事も答えてくれたりしており、やっぱり安定しています
Cursorからも使ったりしているので間接的にサブスクリプションしている事になるのかも

その他にもOperetorのプライバシーポリシーが参考になったり
最近はResponses API、AgentsSDKの発表があったり、やはりOpenAIは先頭走ってる感じがします

#### GitHubCopilot

Cursorと並んで追いかけています
CursorをProプラン月額で契約しているので今は一旦Freeにしていますが
こちらはGitHubでのワークフローを自動化する事に主眼を置いているように見えます
GitHubCopilotWorkspace
↓
GitHubCopilotでの作業/レビュー
↓
CodeAnalyze&GitHubCopilotによる自動修正
の流れですね。GitHubActionもあるのかな？
使用してみないといけないと思っているのでCursorが落ち着いたら触ってみる予定です

#### Ollama

ローカルLMはあまり現状は使用していないのですが、SLMを扱う予定なのでお世話になりそうです
Modelsのトレンドを眺めていると大体AIニュースと一致しています
逆にここで見覚えがないモデルがあると何かしらニュースになっていたりします
(DeepSeekR1は当にそのケース)

#### Microsoft

サービス、という訳ではないんですが挙げておかないといけない気がしており
日々AI系ニュースを見ていると勿論、現状最大シェアOSの持ち主が何もしない訳がなく
…というよりノリノリでAI系実装していってる印象です
~~recallとか中の人絶対ノリノリで実装してる~~

加熱するLM競争から一歩引いて、(OmmniPerser)[https://github.com/microsoft/OmniParser]などLMを繋ぐ環境を整備していきrecallのようなLMが存分に活躍できるようにしていくものを作っていく様子は流石だと思ったので書いておかないといけない気がしました

#### 画像生成系

バリバリは使ってないのですが追いかけはしている感じです
StableDiffusion、Fluxなどなど
そして今日Geminiに画像生成を頼んでみて驚いたり全体的に動きがものすごく早い
また、ComfyUIは設計の考え方が非常に参考になります

#### その他

Difyなどエージェントや仕組み作成に使いそうなものは追いかけています
