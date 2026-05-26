import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import re
import matplotlib.ticker as ticker

def clean_price(price_str):
    if pd.isna(price_str) or '가격 없음' in str(price_str):
        return None
    # 쉼표 등 숫자 이외 문자 제거
    num_str = re.sub(r'[^\d]', '', str(price_str))
    if num_str:
        return int(num_str)
    return None

def extract_resolution(spec_str):
    if pd.isna(spec_str): return '알 수 없음'
    if '4K UHD' in spec_str or '3840' in spec_str: return '4K UHD'
    if 'QHD' in spec_str or '2560' in spec_str: return 'QHD'
    if 'FHD' in spec_str or '1920' in spec_str: return 'FHD'
    return '기타/알 수 없음'

def extract_panel(spec_str):
    if pd.isna(spec_str): return '알 수 없음'
    if 'IPS' in spec_str: return 'IPS'
    if 'QD-VA' in spec_str: return 'QD-VA'
    if 'VA' in spec_str: return 'VA'
    return '기타/알 수 없음'

def extract_refresh_rate(spec_str):
    if pd.isna(spec_str): return '알 수 없음'
    match = re.search(r'(\d+)Hz', spec_str)
    if match:
        return match.group(1) + 'Hz'
    return '알 수 없음'

def main():
    parser = argparse.ArgumentParser(description='Analyze Danawa monitor data')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--output_dir', type=str, default='.', help='Directory to save output files')
    
    args = parser.parse_args()
    input_file = args.input
    output_dir = args.output_dir
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. 데이터 로드 및 전처리
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        return

    # 가격 정제
    df['정제된_가격'] = df['가격'].apply(clean_price)
    
    # 사양 없음 데이터나 가격 정보 없는 데이터 제외
    df_clean = df.dropna(subset=['정제된_가격', '사양']).copy()
    df_clean = df_clean[df_clean['사양'] != '사양 없음']

    # 주요 사양 추출
    df_clean['해상도'] = df_clean['사양'].apply(extract_resolution)
    df_clean['패널'] = df_clean['사양'].apply(extract_panel)
    df_clean['주사율'] = df_clean['사양'].apply(extract_refresh_rate)

    output_csv_path = os.path.join(output_dir, 'analysis_summary.csv')
    df_clean.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"정제된 데이터가 저장되었습니다: {output_csv_path}")

    # 2. 전문적인 시각화 테마 설정
    sns.set_theme(style="whitegrid", context="notebook")
    
    if os.name == 'nt':
        # 윈도우 한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        plt.rcParams['font.family'] = 'AppleGothic'
        
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

    # 제조사별 가격 분포 (Boxplot)
    plt.figure(figsize=(10, 6))
    ax1 = sns.boxplot(data=df_clean, x='제조사', y='정제된_가격', hue='제조사', palette='deep', width=0.5, linewidth=1.5, legend=False)
    plt.title('제조사별 43인치 모니터 가격 분포 및 편차 분석', pad=15, weight='bold', fontsize=16)
    plt.xlabel('')
    plt.ylabel('가격 (원)', fontsize=12)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    sns.despine(left=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_by_manufacturer_boxplot.png'), dpi=300)
    plt.close()

    # 제조사별 평균 가격 (Barplot)
    plt.figure(figsize=(10, 6))
    ax2 = sns.barplot(data=df_clean, x='제조사', y='정제된_가격', hue='제조사', palette='pastel', errorbar=None, width=0.4, legend=False)
    plt.title('제조사별 43인치 모니터 평균 가격 비교', pad=15, weight='bold', fontsize=16)
    plt.xlabel('')
    plt.ylabel('평균 가격 (원)', fontsize=12)
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    sns.despine(left=True)
    
    # 값 표기
    avg_prices = df_clean.groupby('제조사')['정제된_가격'].mean()
    for index, mfg in enumerate(avg_prices.index):
        plt.text(index, avg_prices[mfg] + max(avg_prices)*0.02, f'{int(avg_prices[mfg]):,}원', 
                 ha='center', va='bottom', weight='bold', color='#444444', fontsize=11)
        
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_by_manufacturer_bar.png'), dpi=300)
    plt.close()

    # 해상도 및 패널별 평균 가격
    plt.figure(figsize=(12, 6))
    ax3 = sns.barplot(data=df_clean, x='해상도', y='정제된_가격', hue='패널', palette='Set2', errorbar=None, edgecolor=".2")
    plt.title('해상도 및 패널 종류별 평균 가격 트렌드 분석', pad=15, weight='bold', fontsize=16)
    plt.xlabel('해상도', fontsize=12)
    plt.ylabel('평균 가격 (원)', fontsize=12)
    ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    sns.despine(left=True)
    plt.legend(title='패널 타입', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_by_specs.png'), dpi=300)
    plt.close()

    print("=== 시각화 자료 생성이 완료되었습니다 ===")
    print("생성된 파일 목록:")
    print(f"- {os.path.join(output_dir, 'price_by_manufacturer_boxplot.png')}")
    print(f"- {os.path.join(output_dir, 'price_by_manufacturer_bar.png')}")
    print(f"- {os.path.join(output_dir, 'price_by_specs.png')}")
    
    # 간단한 분석 레포트 텍스트 출력
    print("\n[ 제조사별 요약 통계 ]")
    print(df_clean.groupby('제조사')['정제된_가격'].describe())

if __name__ == "__main__":
    main()
