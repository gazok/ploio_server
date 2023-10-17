# ploio_server
BoB 12th ploio application server repository

<br>
 
## Config

- `python 3.11.4` <br>
- IDE : `Pycharm`, `VSCode` <br>
- Framework : `FastAPI` <br>
- Database : `MySQL` <br>
- ORM : `Sqlalchemy` <br>

<br>

## Agent Data Protocol

> [PROTOCOL](https://github.com/gazok/ploio_agent/blob/master/docs/PROTOCOL.md)

<br>

---

## Docker Image

[Click me](https://github.com/users/oxdjww/packages/container/package/ploio_server)

## Commit Message Convention

### Commit Message Structure

```
type : subject

body

footer
```

<br>
 
#### Type

- add ： 파일 추가
- feat : 새로운 기능 추가
- fix : 버그 수정
- docs : 문서 수정
- style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
- refactor : 코드 리펙토링
- test : 테스트 코드, 리펙토링 테스트 코드 추가
- chore : 빌드 업무 수정, 패키지 매니저 수정

<br>

#### Subject / Body
제목 / 본문

<br>

#### Footer
꼬리말은 optional이고 이슈 트래커 ID를 작성한다.
꼬리말은 "유형: #이슈 번호" 형식으로 사용한다.
여러 개의 이슈 번호를 적을 때는 쉼표(,)로 구분한다.
이슈 트래커 유형은 다음 중 하나를 사용한다.

- Fixes: 이슈 수정중 (아직 해결되지 않은 경우)
- Resolves: 이슈를 해결했을 때 사용
- Ref: 참고할 이슈가 있을 때 사용
- Related to: 해당 커밋에 관련된 이슈번호 (아직 해결되지 않은 경우)
