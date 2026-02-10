# 아직도 가야 할 길 (The Road Less Traveled) - 한국어 번역

이 저장소는 M. 스콧 펙(M. Scott Peck, M.D.) 박사의 고전 지성서이자 심리학 저서인 **"The Road Less Traveled"**(아직도 가야 할 길)를 한국어로 번역하고 Quarto를 사용하여 웹북 형태로 구축한 프로젝트입니다.

## 📖 도서 정보
- **원제:** The Road Less Traveled
- **저자:** M. 스콧 펙 (M. Scott Peck, M.D.)
- **주요 주제:** 훈련(Discipline), 사랑(Love), 종교와 세계관(Religion & Worldviews), 은총(Grace)

## 🌐 웹북 보기
현재 번역된 내용은 아래 링크에서 확인하실 수 있습니다:
**[https://partrita.github.io/road-less-traveled/](https://partrita.github.io/road-less-traveled/)**

## 🛠 프로젝트 구조 및 도구
- **`mybook/`**: Quarto 북 소스 파일 (`.qmd`)이 포함되어 있습니다.
- **Quarto**: 과학 기술 출판 시스템으로, 마크다운을 기반으로 하여 정적 웹사이트, PDF 등을 생성합니다.
- **Pixi**: 프로젝트 의존성 관리 도구입니다 (`quarto` 등 설치).

## 🚀 로컬 실행 방법

### 요구 사항
- [Pixi](https://prefix.dev/)가 설치되어 있어야 합니다.

### 로컬 미리보기
1. 저장소를 클론합니다.
   ```bash
   git clone https://github.com/partrita/road-less-traveled.git
   cd road-less-traveled
   ```
2. Quarto 미리보기를 실행합니다.
   ```bash
   pixi run quarto preview mybook
   ```
3. 자동으로 열리는 브라우저에서 번역된 내용을 확인하실 수 있습니다.

## 📝 번역 및 수정 사항
이 프로젝트는 AI 보조를 받아 원문의 의미를 최대한 살리면서 자연스러운 한국어 문장으로 다듬는 과정을 거쳤습니다. 특히 가독성을 위해 불필요한 줄바꿈을 제거하고, 용어의 일관성을 유지하려 노력했습니다.

## 📄 라이선스
이 프로젝트의 코드는 MIT 라이선스를 따르지만, 도서 원문의 저작권은 저작권자에게 있습니다. 이 프로젝트는 학습 및 공유 목적으로 제작되었습니다.