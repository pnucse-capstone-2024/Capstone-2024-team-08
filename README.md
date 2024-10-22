# 신약 개발 후보물질 발굴을 위한 거대 화합물 라이브러리 탐색 최적화

## 1. 프로젝트 소개
### 1.1. 배경 및 필요성
> &nbsp;신약 개발은 막대한 비용과 긴 시간이 요구되는 복잡한 과정입니다. 그 중에서도 가장 중요한 단계 중 하나는 효과적인 후보물질을 발굴하는 일로, 이는 많은 도전과 난관을 수반합니다. 수억 개가 넘는 방대한 화합물 라이브러리에서 특정 타겟 단백질과 잘 결합할 수 있는 화합물을 찾는 과정은 방대한 시간이 소요됩니다. \
&nbsp;가상 스크리닝 기술과 인공지능 기법이 도입으로 기존 실험 방법보다 시간과 비용을 획기적으로 절감할 수 있었습니다만 여전히 거대한 화합물 라이브러리를 매번 전부 탐색하는 데는 많은 시간이 소요되는 문제가 남아있습니다.

### 1.2. 목표 및 주요 내용
> &nbsp;본 프로젝트의 목표는 방대한 화합물 라이브러리에서 주어진 타겟 단백질과 결합할 가능성이 높은 화합물을 효율적으로 탐색하고 선별하는 것입니다.
사용자가 타겟 단백질 파일을 업로드하면, 해당 단백질과 결합 확률이 가장 높게 예측된 상위 10개의 화합물을 추천합니다.
이를 통해 모든 화합물을 실험하지 않고도, 추천된 일부 화합물의 결합 여부만 실험하여 필요한 화합물을 더 빠르게 찾을 수 있습니다.
프로젝트는 다양한 알고리즘을 제시하고 구현하여, 대규모 라이브러리를 빠르게 탐색하는 동시에 예측의 정확도를 높이는 것을 목표로 합니다.
또한, 사용자 편의를 위해 단백질 파일을 직접 업로드하지 않아도 활용할 수 있는 예제도 제공합니다.


## 2. 상세설계
### 2.1. 시스템 구성도
 ![구상도](https://github.com/user-attachments/assets/a3a8d8bc-a723-4a6a-b1c2-db804826eab9)


### 2.2. 사용 기술
> 각 스택 기술과 버전 기재
> - Django - v5.1

## 3. 설치 및 사용 방법
### 실행 준비
>1. 적절한 위치에 이 리포지토리를 복제
>```
>git clone https://github.com/pnucse-capstone-2024/Capstone-2024-team-08.git
>```
>2. 아래 링크에서 필요한 데이터 압축 파일를 다운로드\
>https://drive.google.com/file/d/1MEfd-uGASIaLedAE2Elr0u-MrPz_hIFg/view?usp=sharing
>3. 압축 파일을 {복제된 리포지토리 경로}/2M/data 에 압축 해제\
예) {repo}/2M/data/db.sqlite3

### 실행 방법
>run.bat 실행\
>첫 실행 시 Docker Image 빌드를 위해 대기 시간이 필요\
>준비 완료 시 자동으로 웹페이지가 열림

### 종료 방법
>shutdown.bat 실행

## 4. 소개 및 시연 영상
[![영상 이름](유튜브 영상 썸네일 URL)](유튜브 영상 URL)
<!--[![부산대학교 정보컴퓨터공학부소개](http://img.youtube.com/vi/zh_gQ_lmLqE/0.jpg)](https://www.youtube.com/watch?v=zh_gQ_lmLqE)    -->
<!--Youtube URL: https://www.youtube.com/watch?v={동영상 ID}-->
<!--Youtube Thumbnail URL: http://img.youtube.com/vi/{동영상 ID}/0.jpg-->

## 5. 팀 소개

> - 이름:   이정민 
> - 학번:   201924656
> - 연락처: jmin5854@gmail.com
> - 역할:   
> 개발 환경 구축 및 관리\
> AutoDockTools, ChimeraX 등을 활용한 프로틴, 리간드 라이브러리 구축\
> spicy.cluster.hierarchy를 활용한 계층적 클러스터링 구현\
> MEMES에 Acquisition Function 추가 구현

> - 이름:   성가빈
> - 학번:   202155565
> - 연락처: bini0408@pusan.ac.kr
> - 역할:  
>rdkit을 이용한 clustering 구현\
MO-MEMES 소스코드 수정 및 MEMES 알고리즘 테스트\
웹 애플리케이션 UI 디자인 및 구현\
MEMES에 Acquisition Function 추가 구현

> - 이름:   최우영
> - 학번:   201845928
> - 연락처: 99wooyoung@naver.com
> - 역할:  
Docker와 Django를 이용해 환경 구축\
리간드 데이터베이스 구축 및 리간드 추가 기능 구현\
웹에서 탐색을 실행할 수 있도록 구현

