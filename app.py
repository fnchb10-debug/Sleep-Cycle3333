from datetime import datetime, timedelta


def get_sleep_cycle() -> int:
    """1단계: 사용자의 수면 사이클(분)을 확인하거나 계산합니다."""
    while True:
        know = input("1. 본인의 수면 사이클(분)을 알고 계신가요? (y/n): ").strip().lower()
        if know in ["y", "yes", "네", "ㅇ"]:
            while True:
                try:
                    cycle = int(input("   수면 사이클(분)을 입력하세요 (예: 90): "))
                    if cycle > 0:
                        return cycle
                    print("   0보다 큰 숫자를 입력해주세요.")
                except ValueError:
                    print("   숫자만 입력해주세요.")

        elif know in ["n", "no", "아니오", "ㄴ"]:
            print("\n   [수면 사이클 찾기]")
            print("   평소 개운하게 잤던 총 수면 시간(n시간)을 입력하면 80, 90, 100분으로 나누어 떨어지는지 확인합니다.")
            while True:
                try:
                    hours = float(input("   개운하게 잤던 수면 시간(시간 단위, 예: 6, 7.5): "))
                    total_minutes = int(round(hours * 60))
                    candidates = [c for c in (80, 90, 100) if total_minutes % c == 0]

                    if candidates:
                        print(f"   -> {total_minutes}분은 {candidates}분으로 나누어 떨어집니다!")
                    else:
                        print(f"   -> {total_minutes}분은 80, 90, 100분으로 딱 나누어 떨어지지 않습니다.")
                        # 가장 근접한 사이클 추천
                        best = min((80, 90, 100), key=lambda c: min(total_minutes % c, c - (total_minutes % c)))
                        print(f"   -> 가장 근접한 추천 사이클은 {best}분입니다.")

                    while True:
                        try:
                            selected = int(input("   사용할 수면 사이클(분)을 입력하세요 (80, 90, 100 중 선택 등): "))
                            if selected > 0:
                                return selected
                            print("   0보다 큰 숫자를 입력해주세요.")
                        except ValueError:
                            print("   숫자만 입력해주세요.")
                except ValueError:
                    print("   숫자 형태로 입력해주세요 (예: 6 또는 7.5).")
        else:
            print("   y 또는 n으로 입력해주세요.")


def parse_time(prompt: str) -> datetime:
    """HH:MM 형식의 문자열을 datetime 객체로 변환합니다."""
    while True:
        time_str = input(prompt).strip()
        try:
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            print("   올바른 시간 형식(HH:MM, 24시간제)으로 입력해주세요. 예: 07:30 또는 23:00")


def main():
    print("=== 수면 사이클 기반 취침/기상 시간 계산기 ===\n")

    # 1. 수면 사이클 결정
    cycle_minutes = get_sleep_cycle()
    print(f"\n-> 설정된 수면 사이클: {cycle_minutes}분\n")

    # 2. 기상시간 vs 취침시간 선택
    while True:
        mode = input("2. 원하는 계산 방식을 선택하세요 (1: 기상 시간 입력 -> 취침 시간 계산 / 2: 취침 시간 입력 -> 기상 시간 계산): ").strip()
        if mode in ["1", "2"]:
            break
        print("   1 또는 2를 입력해주세요.")

    # 3. 시간 입력 및 k회 반복 계산
    if mode == "1":
        target_time = parse_time("\n원하는 기상 시간을 입력하세요 (예: 07:00): ")
        print(f"\n[기상 시간 {target_time.strftime('%H:%M')} 기준 추천 취침 시간]")
        print("-" * 45)
        for k in range(3, 7):  # 3사이클 ~ 6사이클
            sleep_duration = cycle_minutes * k
            bed_time = target_time - timedelta(minutes=sleep_duration)
            hours, mins = divmod(sleep_duration, 60)
            print(f"  {k}사이클 ({hours}시간 {mins:02d}분 수면) -> 취침 추천: {bed_time.strftime('%H:%M')}")

    else:
        target_time = parse_time("\n예정된 취침 시간을 입력하세요 (예: 23:30): ")
        print(f"\n[취침 시간 {target_time.strftime('%H:%M')} 기준 추천 기상 시간]")
        print("-" * 45)
        for k in range(3, 7):  # 3사이클 ~ 6사이클
            sleep_duration = cycle_minutes * k
            wake_time = target_time + timedelta(minutes=sleep_duration)
            hours, mins = divmod(sleep_duration, 60)
            print(f"  {k}사이클 ({hours}시간 {mins:02d}분 수면) -> 기상 추천: {wake_time.strftime('%H:%M')}")


if __name__ == "__main__":
    main()
