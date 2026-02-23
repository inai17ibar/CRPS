# CLAUDE.md — CRPS (Code Reading Practice System)

## プロジェクト概要

CRPS は、エンジニアがコードリーディングスキルを鍛えるための Web アプリケーション。
AI がコードを生成する時代において、コードを「書く」だけでなく「読んで理解する」能力がより重要になっている。
小規模アプリや OSS のコードを題材に、制限時間内に問題に回答する形式で練習できる。

### 問題カテゴリ

- **アルゴリズム・効率化** — コードの計算量分析、パフォーマンス改善、ボトルネック特定
- **システム設計** — アーキテクチャの理解、設計パターンの識別、依存関係の把握

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| フレームワーク | Next.js (App Router) |
| 言語 | TypeScript (strict mode) |
| スタイリング | Tailwind CSS |
| データベース | Prisma + SQLite (開発) / PostgreSQL (本番) |
| 認証 | NextAuth.js |
| テスト | Vitest + Playwright |
| リンター | ESLint + Prettier |
| パッケージ管理 | npm |

## ディレクトリ構成（予定）

```
CRPS/
├── CLAUDE.md                # このファイル
├── src/
│   ├── app/                 # Next.js App Router ページ・レイアウト
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── (auth)/          # 認証関連ページ
│   │   ├── practice/        # 練習画面
│   │   ├── results/         # 結果・振り返り画面
│   │   └── api/             # API Route Handlers
│   ├── components/          # 再利用可能な UI コンポーネント
│   │   ├── ui/              # 汎用 UI (Button, Card, Modal 等)
│   │   ├── code/            # コード表示・ハイライト関連
│   │   └── practice/        # 練習画面固有コンポーネント
│   ├── lib/                 # ユーティリティ・共通ロジック
│   │   ├── db.ts            # Prisma クライアント
│   │   ├── auth.ts          # 認証設定
│   │   └── timer.ts         # タイマーロジック
│   ├── types/               # TypeScript 型定義
│   └── content/             # 練習コンテンツ（問題データ）
│       ├── algorithm/       # アルゴリズム系問題
│       └── system-design/   # システム設計系問題
├── prisma/
│   └── schema.prisma        # データベーススキーマ
├── public/                  # 静的ファイル
├── tests/
│   ├── unit/                # Vitest 単体テスト
│   └── e2e/                 # Playwright E2E テスト
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── .env.local               # 環境変数（Git 管理外）
```

## 開発コマンド

```bash
npm install          # 依存パッケージのインストール
npm run dev          # 開発サーバー起動 (http://localhost:3000)
npm run build        # プロダクションビルド
npm run start        # プロダクションサーバー起動
npm run lint         # ESLint 実行
npm run format       # Prettier 実行
npm run test         # Vitest 単体テスト実行
npm run test:e2e     # Playwright E2E テスト実行
npx prisma migrate dev    # DB マイグレーション（開発）
npx prisma studio         # DB GUI ツール起動
```

## コーディング規約

### TypeScript

- `strict: true` を維持する。`any` は使わない
- 型定義は `src/types/` にまとめる。コンポーネント固有の Props 型は同一ファイル内に定義して良い
- 命名規則:
  - コンポーネント: PascalCase (`CodeViewer.tsx`)
  - ユーティリティ・フック: camelCase (`useTimer.ts`)
  - 型・インターフェース: PascalCase (`type Question`, `interface PracticeSession`)
  - 定数: UPPER_SNAKE_CASE (`MAX_TIME_LIMIT`)

### React / Next.js

- Server Components をデフォルトとし、インタラクティブな部分のみ `"use client"` を使う
- データ取得は Server Components 側で行い、Client Components に props で渡す
- `app/` 配下のページコンポーネントは薄く保ち、ロジックは `lib/` や `components/` に分離する

### コンポーネント設計

- 1 ファイル 1 コンポーネントを基本とする
- UIの汎用コンポーネントは `components/ui/` に配置
- ドメイン固有コンポーネントは `components/<domain>/` に配置

### テスト

- ビジネスロジック（`lib/`）は単体テストを書く
- 主要なユーザーフローは E2E テストでカバーする
- テストファイルは `tests/` ディレクトリに配置する

### Git

- コミットメッセージは英語で、何を・なぜ変更したかを簡潔に書く
- ブランチ名: `feature/xxx`, `fix/xxx`, `refactor/xxx`

## データモデル（概要）

```
User          — ユーザー情報、認証
Question      — 問題データ（コードスニペット、問題文、選択肢、正解、カテゴリ、難易度）
PracticeSession — 練習セッション（ユーザー、開始時刻、制限時間）
Answer        — 回答記録（セッション、問題、ユーザーの回答、正誤、回答時間）
```

## 問題コンテンツ形式

問題データは `src/content/` 配下に JSON または MDX ファイルとして管理する。

```jsonc
{
  "id": "algo-001",
  "category": "algorithm",        // "algorithm" | "system-design"
  "difficulty": "medium",          // "easy" | "medium" | "hard"
  "title": "配列の重複検出",
  "code": "function findDuplicates(arr) { ... }",
  "language": "typescript",
  "timeLimit": 180,                // 秒
  "questions": [
    {
      "text": "この関数の時間計算量は？",
      "options": ["O(n)", "O(n log n)", "O(n²)", "O(1)"],
      "answer": 2
    }
  ]
}
```

## 環境変数

```
DATABASE_URL=         # データベース接続 URL
NEXTAUTH_SECRET=      # NextAuth シークレットキー
NEXTAUTH_URL=         # アプリの URL (http://localhost:3000)
```

## AI アシスタント向けガイドライン

- コード変更前に必ず既存のファイルを読むこと
- `any` 型を導入しない。適切な型を定義する
- 新規ファイルは上記のディレクトリ構成に従って配置する
- テストが存在する場合は、変更後にテストが通ることを確認する
- `.env.local` やシークレット情報をコミットしない
- 不要なコメントやドキュメントを追加しない。コードで意図を表現する
- 問題コンテンツを追加する際は、既存の形式に合わせる
