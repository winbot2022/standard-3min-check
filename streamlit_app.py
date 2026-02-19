# -*- coding: utf-8 -*-
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Any

# =========================
# 1) ピーチベル様専用カスタマイズ（スローな婚活仕様）
# =========================
CONFIG: Dict[str, Any] = {
    "app_title": "ピーチベル様専用：スローに心を整える3分チェック",
    "app_subtitle": "「スローな婚活」を始める前に。いまの心の歩幅を確認してみませんか？",
    "intro_notes": [
        "・点数や評価はありません。",
        "・答えに正解はありません。",
        "・ピーチベルは「急かさない」相談所です。ここで結論を出す必要はありません。",
    ],
    "cta": {
        "title": "焦らなくて大丈夫。このままの気持ちを、一度お話しに来ませんか？",
        "note": "※このチェック結果をそのままお伝えいただくだけで、スムーズにご相談いただけます。",
        "button_label": "ピーチベルの「急かさない」無料相談を予約する",
        "url": "https://www.peach-bell.net/contact/", 
    },
    "footer": "© Victor Consulting × Peach Bell / Slow Marriage Check (Phase0)",
}

# =========================
# 2) 設問定義（ピーチベルのトーンに合わせて微調整）
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
            Option("自分のペースを確認したい", ["整理"]),
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
            Option("ゆっくり整理すれば前に進めそう", ["整理"]),
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
            Option("相談したいが、まだ言葉にできない", ["言語化", "不安"]),
            Option("相談したいが、誰に話すべきか迷う", ["相談先", "迷い"]),
            Option("相談まではいかないが整理したい", ["整理"]),
            Option("いまは自分のペースで考えたい", ["自分軸"]),
        ],
    ),
    Question(
        key="q6",
        title="いま欲しいのはどれに近い？",
        options=[
            Option("自分のペースを大切にしたい", ["休息", "自分軸"]),
            Option("いまの歩幅を客観視したい", ["整理"]),
            Option("気持ちをそのまま受け止めてほしい", ["感情"]),
            Option("焦らずに選択肢を増やしたい", ["選択肢"]),
        ],
    ),
    Question(
        key="q7",
        title="行動に移すとしたら、どれが一番ラク？",
        options=[
            Option("短くメモする", ["言語化"]),
            Option("誰かに少しだけ話す", ["相談先"]),
            Option("一旦休む・距離を置く", ["休息"]),
            Option("ゆっくり優先順位をつける", ["整理"]),
        ],
    ),
    Question(
        key="q8",
        title="今日このチェックで得たいのは？",
        options=[
            Option("気持ちを落ち着かせたい", ["感情", "休息"]),
            Option("考えを整理したい", ["整理", "言語化"]),
            Option("無理に決めず、次の一歩を探したい", ["迷い"]),
            Option("何が引っかかっているか知りたい", ["不安", "整理"]),
        ],
    ),
]

# =========================
# 3) 整理結果生成（ロジック部分は継承し、メッセージをピーチベル仕様に）
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
    if not tags:
        return "いくつか答えてみたことで、いまの気持ちの輪郭が少し見えてきた状態です。"
    if "焦り" in tags and ("不安" in tags or "迷い" in tags):
        return "「スローに進めたい気持ち」と「どこか急いでしまう気持ち」の間で、心が揺れているようです。まずはその揺れを認めることから始めましょう。"
    if "整理" in tags and "言語化" in tags:
        return "考えをゆっくり“言葉に置く”ことで、あなたらしい歩幅を取り戻せそうな流れです。"
    if "感情" in tags:
        return "いまは心の揺れをそのまま受け止める時期かもしれません。ピーチベルは、その揺れを否定しません。"
    return "いまの状況を、焦らずに一つずつ眺められる状態になっています。"

def ordered_points(tags: List[str]) -> List[str]:
    freq: Dict[str, int] = {}
    for t in tags:
        freq[t] = freq.get(t, 0) + 1
    ordered = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [k for k, _ in ordered]

def next_steps(points: List[str]) -> List[str]:
    base = [
        "今日は結論を出さず、いまの気持ちを眺めるだけにする",
        "信頼できる人に「結論なし」で今の気持ちを話してみる",
        "24時間だけ“決めない”と決めて、ゆっくり休む",
    ]
    if "言語化" in points:
        base.insert(0, "気がかりなことを、3つだけ箇条書きにしてみる")
    if "相談先" in points:
        base.append("ピーチベルのような「急かさない相談所」に、そのままの気持ちを伝えてみる")
    if "整理" in points:
        base.append("「自分はどうしたいか」を一番大切に、今の状況を整理してみる")
    
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

    st.subheader("大切にしたいポイント（優先順位）")
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
