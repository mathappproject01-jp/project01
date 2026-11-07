# 最新版
# Dice_Race_Simulater_5.py

import streamlit as st
import random

st.title("🎲 サイコロA vs サイコロB（大ジャンプ値・ゴールマス数を自由設定）競争ゲーム")

# --- ゴールマス数の設定 ---
GOAL = st.slider("ゴールのマス数を選んでください", 20, 200, 40)

# --- サイコロBの大ジャンプ値を設定 ---
jump_value = st.number_input("サイコロBの大ジャンプの値（例：16）", min_value=2, value=16)

# --- セッション状態の初期化 ---
if "wins_A" not in st.session_state:
    st.session_state.wins_A = 0
if "wins_B" not in st.session_state:
    st.session_state.wins_B = 0
if "wins_draw" not in st.session_state:
    st.session_state.wins_draw = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "last_jump_value" not in st.session_state:
    st.session_state.last_jump_value = jump_value
if "last_goal" not in st.session_state:
    st.session_state.last_goal = GOAL

# --- 設定変更時に勝ち数リセット ---
if st.session_state.last_jump_value != jump_value or st.session_state.last_goal != GOAL:
    st.session_state.wins_A = 0
    st.session_state.wins_B = 0
    st.session_state.wins_draw = 0
    st.session_state.game_over = False
    st.session_state.last_jump_value = jump_value
    st.session_state.last_goal = GOAL

# --- サイコロの定義 ---
dice_A = [1, 2, 3, 4, 5, 6]
dice_B = [1, 1, 1, 1, 1, jump_value]

def bar(pos):
    filled = "■" * pos
    empty = "□" * (GOAL - pos)
    return filled + empty

def play_game():
    pos_A = 0
    pos_B = 0
    steps_A = 0
    steps_B = 0
    log = []

    while pos_A < GOAL and pos_B < GOAL:
        roll_A = random.choice(dice_A)
        pos_A = min(pos_A + roll_A, GOAL)
        steps_A += 1
        log.append(f"A：{roll_A} → {pos_A} マス\n{bar(pos_A)}")

        roll_B = random.choice(dice_B)
        pos_B = min(pos_B + roll_B, GOAL)
        steps_B += 1
        log.append(f"B：{roll_B} → {pos_B} マス\n{bar(pos_B)}")

    if pos_A >= GOAL and pos_B < GOAL:
        winner = "A"
    elif pos_B >= GOAL and pos_A < GOAL:
        winner = "B"
    else:
        winner = "同時ゴール"

    return winner, steps_A, steps_B, log, pos_A, pos_B

# --- 勝ち数の表示 ---
st.subheader("📊 勝ち数（累計）")
st.write(f"A の勝ち：{st.session_state.wins_A}")
st.write(f"B の勝ち：{st.session_state.wins_B}")
st.write(f"同時ゴール：{st.session_state.wins_draw}")

# --- ゲーム開始 ---
if not st.session_state.game_over:
    if st.button("ゲーム開始！"):
        winner, steps_A, steps_B, log, pos_A, pos_B = play_game()

        if winner == "A":
            st.session_state.wins_A += 1
        elif winner == "B":
            st.session_state.wins_B += 1
        else:
            st.session_state.wins_draw += 1

        st.session_state.winner = winner
        st.session_state.steps_A = steps_A
        st.session_state.steps_B = steps_B
        st.session_state.log = log
        st.session_state.pos_A = pos_A
        st.session_state.pos_B = pos_B
        st.session_state.game_over = True

# --- 結果表示 ---
if st.session_state.game_over:
    st.subheader(f"🏁 勝者：{st.session_state.winner}")
    st.write(f"Aの手数：{st.session_state.steps_A}")
    st.write(f"Bの手数：{st.session_state.steps_B}")

    st.write("最終位置：")
    st.write(f"A：{st.session_state.pos_A} / {GOAL}")
    st.write(bar(st.session_state.pos_A))
    st.write(f"B：{st.session_state.pos_B} / {GOAL}")
    st.write(bar(st.session_state.pos_B))

    st.write("進行ログ：")
    for line in st.session_state.log:
        st.write(line)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("プレイを続ける(２回クリック)"):
            st.session_state.game_over = False
    with col2:
        if st.button("終了する"):
            st.write("ゲームを終了しました。")
