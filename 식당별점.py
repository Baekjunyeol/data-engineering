import sqlite3
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 윈도우에서 기본적으로 설치된 한글 폰트 이름 지정 (예: 맑은 고딕)
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


# DB 파일명
DB_Name = '학교식당 조사.db'


def connect_db():
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()
    return conn, cur


def create_table():
    conn, cur = connect_db()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS restaurants '
        '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name TEXT NOT NULL,'
        'score REAL NOT NULL CHECK(score >= 1 AND score <= 5))')

    conn.commit()
    conn.close()


def insert_restaurant():
    name = input("맛집 이름을 입력하세요: ")
    while True:
        try:
            score = float(input("평점(1.0~5.0, 소수점 한자리) 입력하세요: "))
            if 1 <= score <= 5:
                score = round(score, 1)
                break
            else:
                print("1 이상 5 이하 숫자를 입력하세요.")
        except:
            print("숫자로 입력해주세요.")

    conn, cur = connect_db()
    cur.execute('INSERT INTO restaurants (name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    conn.close()
    print("등록 완료!")


def list_restaurants():
    conn, cur = connect_db()
    cur.execute('SELECT * FROM restaurants')
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("기록된 맛집이 없습니다.")
        return
    print("ID\t맛집 이름\t평점")
    print("-" * 30)
    for r in rows:
        print(f"{r[0]}\t{r[1]}\t{r[2]}")


def update_restaurant():
    list_restaurants()
    try:
        rid = int(input("수정할 맛집 ID를 입력하세요: "))
    except:
        print("숫자를 입력하세요.")
        return

    conn, cur = connect_db()
    cur.execute('SELECT * FROM restaurants WHERE id = ?', (rid,))
    row = cur.fetchone()
    if not row:
        print("해당 ID가 없습니다.")
        conn.close()
        return

    name = input(f"새로운 이름 입력 (현재: {row[1]}) [그냥 엔터 시 유지]: ")
    if name.strip() == '':
        name = row[1]

    while True:
        score_input = input(f"새로운 평점 입력 (1.0~5.0) (현재: {row[2]}) [그냥 엔터 시 유지]: ")
        if score_input.strip() == '':
            score = row[2]
            break
        try:
            score = float(score_input)
            if 1 <= score <= 5:
                score = round(score, 1)
                break
            else:
                print("1 이상 5 이하 숫자를 입력하세요.")
        except:
            print("숫자로 입력해주세요.")

    cur.execute('UPDATE restaurants SET name = ?, score = ? WHERE id = ?', (name, score, rid))
    conn.commit()
    conn.close()
    print("수정 완료!")


def delete_restaurant():
    list_restaurants()
    try:
        rid = int(input("삭제할 맛집 ID를 입력하세요: "))
    except:
        print("숫자를 입력하세요.")
        return

    conn, cur = connect_db()
    cur.execute('SELECT * FROM restaurants WHERE id = ?', (rid,))
    row = cur.fetchone()
    if not row:
        print("해당 ID가 없습니다.")
        conn.close()
        return

    confirm = input(f"{row[1]}을(를) 삭제할까요? (y/n): ").lower()
    if confirm == 'y':
        cur.execute('DELETE FROM restaurants WHERE id = ?', (rid,))
        conn.commit()
        print("삭제 완료!")
    else:
        print("삭제 취소.")
    conn.close()


def visualize_scores():
    conn, cur = connect_db()
    cur.execute('SELECT score FROM restaurants')
    scores = [row[0] for row in cur.fetchall()]
    conn.close()

    if not scores:
        print("평점 데이터가 없습니다.")
        return

    plt.hist(scores, bins=[0.5 + 0.1 * i for i in range(46)], edgecolor='black')
    plt.title('맛집 평점 분포')
    plt.xlabel('평점')
    plt.ylabel('갯수')
    plt.show()


def main():
    create_table()
    while True:
        print("\n1. 맛집 등록")
        print("2. 맛집 목록")
        print("3. 맛집 수정")
        print("4. 맛집 삭제")
        print("5. 평점 분포 시각화")
        print("6. 종료")
        choice = input("선택: ")

        if choice == '1':
            insert_restaurant()
        elif choice == '2':
            list_restaurants()
        elif choice == '3':
            update_restaurant()
        elif choice == '4':
            delete_restaurant()
        elif choice == '5':
            visualize_scores()
        elif choice == '6':
            print("종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()