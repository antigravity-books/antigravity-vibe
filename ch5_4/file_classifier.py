# -*- coding: utf-8 -*-
"""
Downloads 폴더 파일 자동 분류 시스템
- 주간보고서, 회의록, 재무문서를 팀별/유형별로 분류
- 기타 파일은 ETC 폴더로 통합
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import re

# Windows 콘솔 UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class FileClassifier:
    """파일 분류기 클래스"""
    
    def __init__(self, source_dir, target_base_dir):
        """
        Args:
            source_dir: 분류할 파일이 있는 소스 디렉토리 (Downloads)
            target_base_dir: 분류된 파일을 저장할 기본 디렉토리 (ch5_4)
        """
        self.source_dir = Path(source_dir)
        self.target_base_dir = Path(target_base_dir)
        self.documents_dir = self.target_base_dir / "ClassifiedFiles" / "Documents"
        self.logs_dir = self.target_base_dir / "ClassifiedFiles" / "ClassificationLogs"
        
        # 통계 정보
        self.stats = {
            'total': 0,
            'reports': 0,
            'minutes': 0,
            'financial': 0,
            'etc': 0,
            'errors': 0
        }
        
        # 팀 목록
        self.teams = ['개발팀', '기획팀', '마케팅팀', '영업1팀', '영업2팀']
        
    def create_folder_structure(self):
        """필요한 폴더 구조 생성"""
        print("\n[폴더 구조 생성 중...]")
        
        # Reports 폴더 (팀별)
        for team in self.teams:
            folder = self.documents_dir / "Reports" / team
            folder.mkdir(parents=True, exist_ok=True)
            print(f"  OK {folder}")
        
        # Minutes 폴더 (팀별)
        for team in self.teams:
            folder = self.documents_dir / "Minutes" / team
            folder.mkdir(parents=True, exist_ok=True)
            print(f"  OK {folder}")
        
        # Financial 폴더
        financial_folders = ['Transactions', 'Sales', 'Inventory']
        for subfolder in financial_folders:
            folder = self.documents_dir / "Financial" / subfolder
            folder.mkdir(parents=True, exist_ok=True)
            print(f"  OK {folder}")
        
        # ETC 폴더
        etc_folder = self.documents_dir / "ETC"
        etc_folder.mkdir(parents=True, exist_ok=True)
        print(f"  OK {etc_folder}")
        
        # Logs 폴더
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        print(f"  OK {self.logs_dir}")
        
        print("[완료] 폴더 구조 생성 완료!\n")
    
    def extract_team_name(self, filename):
        """파일명에서 팀명 추출"""
        for team in self.teams:
            if team in filename:
                return team
        return None
    
    def classify_file(self, filename):
        """
        파일명을 분석하여 대상 폴더 결정
        
        Returns:
            tuple: (target_folder_path, category)
        """
        # 1. 주간보고서 분류
        if '주간보고' in filename:
            team = self.extract_team_name(filename)
            if team:
                return self.documents_dir / "Reports" / team, 'reports'
        
        # 2. 주간회의록 분류
        if '주간회의록' in filename:
            team = self.extract_team_name(filename)
            if team:
                return self.documents_dir / "Minutes" / team, 'minutes'
        
        # 3. 재무 문서 분류 (XLSX)
        if filename.endswith('.xlsx'):
            # 거래 관련
            if any(keyword in filename for keyword in ['거래명세서', '견적서', '발주서']):
                return self.documents_dir / "Financial" / "Transactions", 'financial'
            
            # 매출 관련
            if any(keyword in filename for keyword in ['매출집계', '판매실적']):
                return self.documents_dir / "Financial" / "Sales", 'financial'
            
            # 재고 관련
            if any(keyword in filename for keyword in ['입고현황', '재고현황', '출고현황', '주문요청']):
                return self.documents_dir / "Financial" / "Inventory", 'financial'
        
        # 4. 기타 모든 파일 → ETC
        return self.documents_dir / "ETC", 'etc'
    
    def move_file(self, source_path, target_folder, dry_run=True):
        """
        파일을 대상 폴더로 이동
        
        Args:
            source_path: 원본 파일 경로
            target_folder: 대상 폴더 경로
            dry_run: True면 실제 이동 안함 (테스트 모드)
        """
        target_path = target_folder / source_path.name
        
        if dry_run:
            print(f"  [테스트] {source_path.name} -> {target_folder.relative_to(self.target_base_dir)}")
        else:
            try:
                shutil.copy2(source_path, target_path)
                print(f"  [OK] {source_path.name} -> {target_folder.relative_to(self.target_base_dir)}")
            except Exception as e:
                print(f"  [오류] {source_path.name} - {e}")
                self.stats['errors'] += 1
    
    def run(self, dry_run=True):
        """
        파일 분류 실행
        
        Args:
            dry_run: True면 테스트 모드 (실제 파일 이동 안함)
        """
        mode = "테스트 모드" if dry_run else "실행 모드"
        print(f"\n{'='*60}")
        print(f"[시작] 파일 분류 - {mode}")
        print(f"{'='*60}")
        print(f"소스 폴더: {self.source_dir}")
        print(f"대상 폴더: {self.target_base_dir / 'ClassifiedFiles'}")
        
        # 폴더 구조 생성
        self.create_folder_structure()
        
        # 로그 파일 준비
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"classification_{timestamp}.log"
        log_entries = []
        
        # 파일 목록 가져오기
        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        self.stats['total'] = len(files)
        
        print(f"\n총 {self.stats['total']}개 파일 분류 중...\n")
        
        # 각 파일 분류
        for file_path in files:
            target_folder, category = self.classify_file(file_path.name)
            
            # 통계 업데이트
            self.stats[category] += 1
            
            # 파일 이동
            self.move_file(file_path, target_folder, dry_run)
            
            # 로그 기록
            log_entry = f"{datetime.now().isoformat()} | {file_path.name} | {category} | {target_folder.relative_to(self.target_base_dir)}"
            log_entries.append(log_entry)
        
        # 로그 파일 저장
        if not dry_run:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"파일 분류 로그 - {timestamp}\n")
                f.write(f"{'='*80}\n\n")
                for entry in log_entries:
                    f.write(entry + '\n')
            print(f"\n로그 파일 저장: {log_file.name}")
        
        # 결과 출력
        self.print_summary(dry_run)
    
    def print_summary(self, dry_run):
        """분류 결과 요약 출력"""
        print(f"\n{'='*60}")
        print("[분류 결과 요약]")
        print(f"{'='*60}")
        print(f"총 파일 수:      {self.stats['total']:>3}개")
        print(f"주간보고서:      {self.stats['reports']:>3}개")
        print(f"주간회의록:      {self.stats['minutes']:>3}개")
        print(f"재무 문서:       {self.stats['financial']:>3}개")
        print(f"기타 파일(ETC):  {self.stats['etc']:>3}개")
        if self.stats['errors'] > 0:
            print(f"오류 발생:       {self.stats['errors']:>3}개")
        print(f"{'='*60}")
        
        if dry_run:
            print("\n[주의] 테스트 모드로 실행되었습니다.")
            print("   실제 파일을 이동하려면 dry_run=False로 설정하세요.")
        else:
            print("\n[완료] 파일 분류가 완료되었습니다!")
    
    def print_stats(self):
        """분류 통계만 출력 (파일 이동 없이)"""
        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        
        stats = {
            'reports': {},
            'minutes': {},
            'financial': {'Transactions': 0, 'Sales': 0, 'Inventory': 0},
            'etc': 0
        }
        
        for team in self.teams:
            stats['reports'][team] = 0
            stats['minutes'][team] = 0
        
        for file_path in files:
            filename = file_path.name
            
            # 주간보고서
            if '주간보고' in filename:
                team = self.extract_team_name(filename)
                if team:
                    stats['reports'][team] += 1
            
            # 주간회의록
            elif '주간회의록' in filename:
                team = self.extract_team_name(filename)
                if team:
                    stats['minutes'][team] += 1
            
            # 재무 문서
            elif filename.endswith('.xlsx'):
                if any(k in filename for k in ['거래명세서', '견적서', '발주서']):
                    stats['financial']['Transactions'] += 1
                elif any(k in filename for k in ['매출집계', '판매실적']):
                    stats['financial']['Sales'] += 1
                elif any(k in filename for k in ['입고현황', '재고현황', '출고현황', '주문요청']):
                    stats['financial']['Inventory'] += 1
                else:
                    stats['etc'] += 1
            
            # 기타
            else:
                stats['etc'] += 1
        
        # 통계 출력
        print("\n[파일 분류 통계 (미리보기)]")
        print("="*60)
        
        print("\n[주간보고서]")
        for team, count in stats['reports'].items():
            if count > 0:
                print(f"  {team}: {count}개")
        
        print("\n[주간회의록]")
        for team, count in stats['minutes'].items():
            if count > 0:
                print(f"  {team}: {count}개")
        
        print("\n[재무 문서]")
        for category, count in stats['financial'].items():
            if count > 0:
                print(f"  {category}: {count}개")
        
        print(f"\n[기타 파일(ETC)]: {stats['etc']}개")
        print("="*60)


def main():
    """메인 실행 함수"""
    # 경로 설정
    downloads_dir = r"C:\Users\USER\Downloads"
    ch5_4_dir = r"C:\Users\USER\OneDrive\Desktop\Project\vibe_coding_antigravity\ch5_4"
    
    # 파일 분류기 생성
    classifier = FileClassifier(downloads_dir, ch5_4_dir)
    
    # 실행 모드 선택
    print("\n" + "="*60)
    print("Downloads 폴더 파일 자동 분류 시스템")
    print("="*60)
    print("\n실행 모드를 선택하세요:")
    print("1. 통계만 보기 (파일 이동 없음)")
    print("2. 테스트 모드 (파일 이동 미리보기)")
    print("3. 실행 모드 (실제 파일 복사)")
    
    choice = input("\n선택 (1/2/3): ").strip()
    
    if choice == '1':
        classifier.print_stats()
    elif choice == '2':
        classifier.run(dry_run=True)
    elif choice == '3':
        confirm = input("\n[주의] 실제로 파일을 복사합니다. 계속하시겠습니까? (y/n): ").strip().lower()
        if confirm == 'y':
            classifier.run(dry_run=False)
        else:
            print("[취소] 취소되었습니다.")
    else:
        print("[오류] 잘못된 선택입니다.")


if __name__ == "__main__":
    main()
