# -*- coding: utf-8 -*-
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Any

# =========================
# 1) 差し替え集約（ここだけ触れば 1社専用化できる）
# =========================
CONFIG: Dict[str, Any] = {
    "app_title": "3分で気持ちを整理",
    "app_subtitle": "相談する前に、いまの状況を言葉にしてみるためのチェックです。",
    "intro_notes": [
        "・点数や評価はありません。",
        "・答えに正解はありません。",
        "・ここで結論を出す必要はありません。",
    ],
    "cta": {
        "title": "一度、気持ちを整理してみませんか？",
        "note": "※ここは後で、契約先（1社専用）の名称・リンクに差し替えます",
        "button_label": "相談窓口を見る（仮）",
        "url": "https://example.com",  # 仮リンク
    },
    "footer": "© Victor Consulting / Standard 3min-check (Phase0)",
}

# =========================
# 2) 設問定義（8問：将来10問に増やしてもここを増やすだけ）
#    - 各選択肢に「気になるポイント（タグ）」を紐づける
#    - タグは“評価”ではなく “整理の観点” として扱う
# =========================
@dataclass
class Option:
    label: str
    tags: List[str]

@dataclass
class Question:
    key: str
    title: str
    options: List[Option]

QUESTIONS: List[Question] = [
    Question(
        key="q1",
        title="いまの気持ちに一番近いものは？",
        options=[
            Option("少し不安がある", ["不安"]),
            Option("迷いが続いている", ["迷い"]),
            Option("焦りがある", ["焦り"]),
            Option("落ち着いているが確認したい", ["整理"]),
        ],
    ),
    Question(
        key="q2",
        title="気になっているのはどんなこと？",
        options=[
            Option("相手との関係性", ["関係性"]),
            Option("自分の気持ちの揺れ", ["感情"]),
            Option("将来の見通し", ["将来"]),
            Option("周囲の目・比較", ["周囲"]),
        ],
    ),
    Question(
        key="q3",
        title="いま、頭の中はどんな状態？",
        options=[
            Option("情報が多くて混乱している", ["混乱"]),
            Option("考えが堂々巡りしている", ["迷い"]),
            Option("決めなきゃと追われている", ["焦り"]),
            Option("整理すれば前に進めそう", ["整理"]),
        ],
    ),
    Question(
        key="q4",
        title="いま一番しんどいのは？",
        options=[
            Option("気持ちの上下が大きい", ["感情"]),
            Option("相手の気持ちが読めない", ["関係性", "不安"]),
            Option("自分の判断に自信がない", ["不安", "迷い"]),
            Option("時間だけが過ぎていく感覚", ["焦り"]),
        ],
    ),
    Question(
        key="q5",
        title="相談したい気持ちはありますか？",
        options=[
            Option("相談したいが、まだ言語化できない", ["言語化", "不安"]),
            Option("相談したいが、誰に話すべきか迷う", ["相談先", "迷い"]),
            Option("相談まではいかないが整理したい", ["整理"]),
            Option("いまは一人で考えたい", ["自分軸"]),
        ],
    ),
    Question(
        key="q6",
        title="いま欲しいのはどれに近い？",
        options=[
            Option("背中を押してほしい", ["後押し", "焦り"]),
            Option("状況を客観視したい", ["整理"]),
            Option("気持ちを受け止めてほしい", ["感情"]),
            Option("選択肢を増やしたい", ["選択肢"]),
        ],
    ),
    Question(
        key="q7",
        title="行動に移すとしたら、どれが一番ラク？",
        options=[
            Option("短くメモする", ["言語化"]),
            Option("誰かに少しだけ話す", ["相談先"]),
            Option("一旦休む・距離を置く", ["休息"]),
            Option("情報を整理して優先順位をつける", ["整理"]),
        ],
    ),
    Question(
        key="q8",
        title="今日このチェックで得たいのは？",
        options=[
            Option("気持ちを落ち着かせたい", ["感情", "休息"]),
            Option("考えを整理したい", ["整理", "言語化"]),
            Option("次の一歩を決めたいが、決め切れない", ["迷い"]),
            Option("何が引っかかっているか知りたい", ["不安", "整理"]),
        ],
    ),
]

# =========================
# 3) 整理結果生成（評価ではなく “観点の抽出”）
# =========================
def collect_tags(answers: Dict[str, str]) -> List[str]:
    tags: List[str] = []
    option_map: Dict[str, Dict[str, List[str]]] = {}
    for q in QUESTIONS:
        option_map[q.key] = {opt.label: opt.tags for opt in q.options}

    for q in QUESTIONS:
        a = answers.get(q.key)
        if not a:
            continue
        tags.extend(option_map[q.key].get(a, []))
    return tags

def summarize_state(tags: List[str]) -> str:
    # できるだけ“断定・評価”を避けた短文
    # タグの傾向に応じて言い回しだけ変える（点数/タイプ化しない）
    if not tags:
        return "いくつか答えてみたことで、いまの気持ちの輪郭が少し見えてきた状態です。"
    if "焦り" in tags and ("不安" in tags or "迷い" in tags):
        return "「急いだほうがいい気持ち」と「慎重になりたい気持ち」が同時に動いているようです。"
    if "整理" in tags and "言語化" in tags:
        return "考えを“言葉に置く”ことで、気持ちが落ち着いていきそうな流れです。"
    if "感情" in tags:
        return "いまは気持ちの揺れがポイントになっていそうです。まずは受け止めるだけでも十分です。"
    return "いまの状況を“整理の観点”に分けて眺められる状態になっています。"

def ordered_points(tags: List[str]) -> List[str]:
    # 順番は出してよいが、数値は出さない
    freq: Dict[str, int] = {}
    for t in tags:
        freq[t] = freq.get(t, 0) + 1
    # 出現回数の多い順（同数は安定ソート）
    ordered = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [k for k, _ in ordered]

def next_steps(points: List[str]) -> List[str]:
    # 行動を強制しない “選択肢” を提示
    base = [
        "今日は結論を出さず、「何が気になっているか」だけをメモに残す",
        "信頼できる人に、結論なしで「いまの気持ち」だけ話してみる",
        "24時間だけ“決めない”と決めて、休んでからもう一度考える",
    ]
    # 観点に応じて、軽い提案を1つだけ足す（断定しない）
    if "言語化" in points:
        base.insert(0, "頭の中の言葉を、箇条書きで3行だけ書き出してみる")
    if "相談先" in points:
        base.append("相談するなら「結論を急がない相談」であることを先に伝える")
    if "整理" in points:
        base.append("気になる点を「自分／相手／周囲／将来」に分けて眺めてみる")
    # 重複を除去しつつ順番維持
    seen = set()
    uniq = []
    for x in base:
        if x not in seen:
            uniq.append(x); seen.add(x)
    return uniq[:5]

# =========================
# 4) UI
# =========================
def main():
    st.set_page_config(page_title=CONFIG["app_title"], layout="centered")

    st.title(CONFIG["app_title"])
    st.caption(CONFIG["app_subtitle"])

    with st.expander("このチェックについて", expanded=True):
        for line in CONFIG["intro_notes"]:
            st.write(line)

    st.divider()

    st.subheader("質問（3分）")
    answers: Dict[str, str] = {}

    for i, q in enumerate(QUESTIONS, start=1):
        st.write(f"**Q{i}. {q.title}**")
        labels = [opt.label for opt in q.options]
        ans = st.radio(
            label="",
            options=labels,
            index=None,
            key=q.key,
            horizontal=False,
        )
        if ans:
            answers[q.key] = ans
        st.write("")

    st.divider()

    can_show = (len(answers) == len(QUESTIONS))
    if not can_show:
        st.info("すべての質問に答えると、整理結果が表示されます。")
        return

    tags = collect_tags(answers)
    points = ordered_points(tags)

    st.subheader("いまの状態の整理")
    st.write(summarize_state(tags))
    st.write("**ここで結論を出す必要はありません。**")

    st.subheader("気にしているポイント（順番）")
    if points:
        for idx, p in enumerate(points, start=1):
            st.write(f"{idx}. {p}")
    else:
        st.write("いくつかの観点が見えてきました。")

    st.subheader("次の一歩（選択肢）")
    for s in next_steps(points):
        st.write(f"・{s}")

    st.divider()

    st.subheader(CONFIG["cta"]["title"])
    st.caption(CONFIG["cta"]["note"])
    st.link_button(CONFIG["cta"]["button_label"], CONFIG["cta"]["url"])

    st.caption(CONFIG["footer"])

if __name__ == "__main__":
    main()













