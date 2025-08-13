# SeoulOD_Vis

---

## ⏱️ Overview of SeoulOD Visualization Tool
<img src="https://github.com/user-attachments/assets/1cf2065f-5ab9-423b-a533-a7763b4c439b">

---

## 📑 프로젝트 소개
### 👤 서울 인구이동 시각화 프로그램
1. **데이터**  
   - **KT 서울 이동 데이터**: 2019~2022년 서울시 전역의 이동 정보 포함  
   - 휴대폰과 기지국 간 통신 데이터를 기반으로 수집  
   - 행정동 단위보다 약 4배 세밀한 공간 단위인 **교통 폴리곤** 단위 데이터 사용  

2. **SeoulOD-Vis 시각화 도구 기능**  
   - **지도 시각화**: 이동 흐름 및 지역별 이동 현황을 Flowmap, Heatmap 형태로 시각화  
   - **조건 선택**: 시간, 요일, 계절, 지역 등 다양한 조건에 따른 필터링 제공  
   - **상세 정보 표시**: 특정 이동 경로나 구역의 세부 통계 데이터 확인 가능  

---

> **특징**  
> - 대규모 이동 데이터(약 수억 건)를 효율적으로 처리하는 최적화된 시각화 엔진  
> - 다양한 공간·시간 조건을 조합하여 맞춤형 분석 가능  
> - 고해상도 교통 폴리곤 단위 데이터로 정밀한 공간 분석 지원  
> - Flask 기반 웹 애플리케이션으로, 브라우저에서 바로 접근 가능  

---

## 🛠 사용 기술 스택
- **Language** : Python, JavaScript  
- **Framework** : Flask  
- **Visualization** : Mapbox GL JS, Deck.gl
