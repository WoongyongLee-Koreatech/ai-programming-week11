import pytest
from load_scores import load_scores

def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),   # 경계 바로 아래
    (0,   True),    # ★ 아래쪽 경계
    (1,   True),
    (99,  True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
    (102, False),
    (10000, False)
])
def test_점수_경계값(점수, 유효한가, tmp_path):
    파일 = tmp_path / "임시.csv"
    파일.write_text(f"이름,점수\n테스트,{점수}\n", encoding="utf-8")
    kept, skipped = load_scores(파일)
    assert (len(kept) == 1) == 유효한가
