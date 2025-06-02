import requests
import json
import time

def get_all_youth_policies(
    api_key: str,
    file_name: str = "all_policy_data.json",
    page_size: int = 100,
    page_type: str = "1",
    rtn_type: str = "json",
):
    url = "https://www.youthcenter.go.kr/go/ythip/getPlcy"
    all_policies = []
    page_num = 1

    while True:
        params = {
            "apiKeyNm": api_key,
            "pageNum": page_num,
            "pageSize": page_size,
            "pageType": page_type,
            "rtnType": rtn_type,
        }

        try:
            response = requests.get(url, params=params, verify=False)
            response.raise_for_status()
            data = response.json()
            
            policies = data.get("result", {}).get("youthPolicyList", [])
            if not policies:
                print(f"[완료] 더 이상 가져올 데이터가 없습니다. 마지막 페이지: {page_num}")
                break

            all_policies.extend(policies)
            print(f"{page_num}페이지에서 {len(policies)}개 수집 (누적: {len(all_policies)})")
            page_num += 1

            # 서버에 부담을 줄이기 위한 sleep
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"요청 실패 (페이지 {page_num}): {e}")
            break

    # 모든 정책을 하나의 JSON 파일로 저장
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(all_policies, f, ensure_ascii=False, indent=2)

    print(f"총 {len(all_policies)}개의 정책이 '{file_name}'에 저장되었습니다.")

# 사용 예시
if __name__ == "__main__":
    API_KEY = "API key 발급 필요"
    get_all_youth_policies(
        api_key=API_KEY,
        file_name="all_policy_data.json",
        page_size=100,
    )