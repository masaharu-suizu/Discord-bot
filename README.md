# リポジトリの説明

自分のDiscordのBotを管理するためのリポジトリ。<br>
DiscordのWeb hookの機能を使用している。<br>
GitHub Actionsの使い捨て仮想マシンにcronを設定して動作させている。

## Botの内容

* 株のマーケットがCloseした後に、保有している株に関する情報を知らせるBot

Botのフォーマット
```text
株価終値チェック (YYYY-MM-DD)

{{銘柄名}}
購入金額: xxx円
終値: xxxx円 (購入比: +xxx円、 前日比 +xx円)
資産額: xxxxxxxx円


{{銘柄名}}
購入金額: xxx円
終値: xxxx円 (購入比: +xxx円、 前日比 +xx円)
資産額: xxxxxxxx円


-------------
総資産サマリー
総資産額: xxxxxxxxx円 (前日比: +xxxxx円)
評価損益: +xxxxx円
```

[GitHub Actions](https://github.com/masaharu-suizu/Discord-bot/blob/main/.github/workflows/daily_report.yml)

* 毎週金曜日に保有している株に関する週間レポートを送るBot

Botのフォーマット
```text
週間レポート (前週比)
実行日 YYYY-MM-DD

{{銘柄名}}
前週比: +xxxxx円


{{銘柄名}}
前週比: +xxxxx円


-------------
総資産サマリー
総資産額: xxxxxxxxx円
前週比: +xxxxx円
```

[GitHub Actions](https://github.com/masaharu-suizu/Discord-bot/blob/main/.github/workflows/weekly_report.yml)

# その他

GrypeでSBOMをスキャンしPythonパッケージの脆弱性を見るけるGitHub Actionsも動かしている。もし脆弱性が見つかった場合はDiscordに通知が飛ぶようにしている。
[GitHub Actions](https://github.com/masaharu-suizu/Discord-bot/blob/main/.github/workflows/security-scan.yml)