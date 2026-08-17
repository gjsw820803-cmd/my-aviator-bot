import os
import glob
import time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def find_latest_csv():
    """
    Downloads folder එකෙහි සහ Project folder එකෙහි ඇති 
    'aviator' නමින් පටන්ගන්නා CSV files අතුරින් අලුත්ම (Most Recent) File එක සොයා ගනී.
    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    
    candidate_files = []
    
    # 1. Downloads folder එකෙන් aviator*.csv සොයා ගැනීම
    if os.path.exists(downloads_dir):
        dl_files = glob.glob(os.path.join(downloads_dir, "*aviator*.csv"))
        candidate_files.extend(dl_files)
        
    # 2. Project folder එකෙනුත් සොයා ගැනීම
    proj_files = glob.glob(os.path.join(project_dir, "*aviator*.csv"))
    candidate_files.extend(proj_files)
    
    # 3. 'aviator' නමින් නැති වුණොත් වෙනත් ඕනෑම CSV file එකක් බැලීම (Fallback)
    if not candidate_files:
        if os.path.exists(downloads_dir):
            candidate_files.extend(glob.glob(os.path.join(downloads_dir, "*.csv")))
        candidate_files.extend(glob.glob(os.path.join(project_dir, "*.csv")))
    
    if not candidate_files:
        print("⚠️ No CSV file found in Downloads or Project directory!")
        return None
        
    latest_file = max(candidate_files, key=os.path.getmtime)
    print(f"📁 Auto-detected Latest CSV: {os.path.basename(latest_file)}")
    return latest_file


def get_df():
    """CSV File එක Read කර Header Names Clean කර DataFrame එක Return කරයි"""
    csv_file = find_latest_csv()
    if not csv_file or not os.path.exists(csv_file):
        return pd.DataFrame(), "No CSV found"
    
    try:
        df = pd.read_csv(csv_file)
        if df.empty:
            return pd.DataFrame(), csv_file
            
        # Header names lowercase කර clean කිරීම
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df, csv_file
    except Exception as e:
        print(f"❌ Error reading CSV {csv_file}: {e}")
        return pd.DataFrame(), csv_file


def get_crash_col_name(df):
    """Crash/Multiplier values අඩංගු Column Name එක නිවැරදිව සොයා ගනී"""
    if df.empty:
        return None
        
    # 1. 'round' නොවන crash/multiplier අඩංගු column එක සොයයි
    for col in df.columns:
        c_clean = col.lower().strip()
        if c_clean in ["round", "id", "num", "round_no", "timestamp"]:
            continue
        if any(k in c_clean for k in ["crash", "multiplier", "odd", "coef", "payout", "val", "x"]):
            return col
            
    # 2. 'round' නොවන වෙනත් numeric column එකක් තිබේදැයි බලයි
    for col in df.columns:
        c_clean = col.lower().strip()
        if c_clean in ["round", "id", "num", "round_no", "timestamp"]:
            continue
        s = pd.to_numeric(df[col].astype(str).str.replace('x', '', case=False).str.strip(), errors='coerce').dropna()
        if len(s) > 0:
            return col
            
    return None


def get_crash_series(df):
    """Crash/Multiplier values numeric series එක Return කරයි"""
    col = get_crash_col_name(df)
    if col and col in df.columns:
        s = df[col].astype(str).str.replace('x', '', case=False).str.strip()
        return pd.to_numeric(s, errors='coerce').dropna()
    return pd.Series(dtype=float)


def load_crash_values():
    """Charts සහ Analytics සඳහා Crash values list එක ලබාදෙයි"""
    df, _ = get_df()
    series = get_crash_series(df)
    return series.tolist()


def calculate_statistics():
    values = load_crash_values()
    if not values:
        return {
            "total_rounds": 0,
            "average": 0.0,
            "below_2": 0.0,
            "between_2_5": 0.0,
            "between_5_10": 0.0,
            "above_10": 0.0
        }

    total = len(values)
    avg = sum(values) / total
    below_2 = (sum(1 for x in values if x < 2.0) / total) * 100
    b_2_5 = (sum(1 for x in values if 2.0 <= x < 5.0) / total) * 100
    b_5_10 = (sum(1 for x in values if 5.0 <= x < 10.0) / total) * 100
    above_10 = (sum(1 for x in values if x >= 10.0) / total) * 100

    return {
        "total_rounds": total,
        "average": avg,
        "below_2": below_2,
        "between_2_5": b_2_5,
        "between_5_10": b_5_10,
        "above_10": above_10
    }


def get_recent_crash_history(limit=10):
    df, _ = get_df()
    if df.empty:
        return []
    
    crash_col = get_crash_col_name(df)
    if not crash_col:
        return []

    round_col = next((c for c in df.columns if c.lower() in ["round", "id", "num", "round_no", "index", "#", "game_id"]), None)
    time_col = next((c for c in df.columns if c.lower() in ["time", "timestamp", "datetime", "date", "created_at"]), None)
        
    history = []
    valid_df = df.dropna(subset=[crash_col]).tail(limit).iloc[::-1]
    
    for idx, row in valid_df.iterrows():
        round_val = row[round_col] if round_col and pd.notna(row[round_col]) else (idx + 1)
        
        # Crash Value Format කිරීම
        raw_crash = str(row[crash_col]).replace('x', '').replace('X', '').strip()
        try:
            crash_val = float(raw_crash)
            crash_str = f"{crash_val:.2f}x"
        except Exception:
            crash_str = str(row[crash_col])
            
        # Time String Format කිරීම (නියමිත වේලාවම පෙන්වීම)
        time_val = str(row[time_col]).strip() if time_col and pd.notna(row[time_col]) else "N/A"
            
        history.append({
            "round": round_val,
            "crash": crash_str,
            "time": time_val
        })
    return history

# Function Aliases
get_crash_history = get_recent_crash_history


def generate_crash_chart(limit=30, output_path="crash_chart.png"):
    """
    අන්තිම rounds 30 (හෝ limit) වල Crash Values Plot කර Chart Image එකක් Generate කරයි
    """
    values = load_crash_values()
    if not values:
        return None
        
    recent_values = values[-limit:]
    rounds = list(range(1, len(recent_values) + 1))
    
    plt.figure(figsize=(10, 5), dpi=100)
    plt.plot(rounds, recent_values, marker='o', color='#ff4757', linewidth=2, label='Multiplier (x)')
    plt.axhline(y=2.0, color='#ffa502', linestyle='--', label='2.00x Threshold')
    
    plt.title('Aviator Crash Multiplier History (Recent Rounds)', fontsize=14, fontweight='bold')
    plt.xlabel('Round Count', fontsize=12)
    plt.ylabel('Multiplier (x)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    chart_file = os.path.join(project_dir, output_path)
    plt.savefig(chart_file)
    plt.close()
    
    return chart_file

# Function Aliases
get_crash_chart = generate_crash_chart
create_crash_chart = generate_crash_chart


def get_statistical_analysis():
    values = load_crash_values()
    if not values:
        return {
            "total": 0,
            "average": 0.0,
            "median": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
            "std_dev": 0.0,
            "longest_low_run": 0,
            "longest_high_run": 0
        }

    curr_low = max_low = 0
    curr_high = max_high = 0
    for x in values:
        if x < 2.0:
            curr_low += 1
            max_low = max(max_low, curr_low)
        else:
            curr_low = 0

        if x >= 10.0:
            curr_high += 1
            max_high = max(max_high, curr_high)
        else:
            curr_high = 0

    return {
        "total": len(values),
        "average": float(np.mean(values)),
        "median": float(np.median(values)),
        "minimum": float(min(values)),
        "maximum": float(max(values)),
        "std_dev": float(np.std(values)),
        "longest_low_run": max_low,
        "longest_high_run": max_high
    }


def get_historical_insights():
    values = load_crash_values()
    if not values:
        return None

    avg20 = sum(values[-20:]) / len(values[-20:]) if len(values) >= 1 else 0.0
    avg50 = sum(values[-50:]) / len(values[-50:]) if len(values) >= 1 else 0.0
    overall = sum(values) / len(values)

    trend = "Stable ➡️"
    if avg20 > avg50:
        trend = "Uptrend 📈"
    elif avg20 < avg50:
        trend = "Downtrend 📉"

    return {
        "average20": avg20,
        "average50": avg50,
        "overall_average": overall,
        "highest": max(values),
        "lowest": min(values),
        "trend": trend
    }


def get_refresh_status():
    df, csv_file = get_df()
    values = load_crash_values()
    file_name = os.path.basename(csv_file) if csv_file else "None"
    return {
        "status": "Active 🟢",
        "last_updated": time.strftime("%H:%M:%S"),
        "total_rounds": len(values),
        "new_rounds": 0,
        "file_name": file_name
    }


def get_data_quality():
    df, csv_file = get_df()
    total = len(df)
    if total == 0:
        return {
            "total_rows": 0,
            "valid_rows": 0,
            "invalid_rows": 0,
            "duplicate_rows": 0
        }

    valid = len(load_crash_values())
    invalid = max(0, total - valid)
    duplicates = int(df.duplicated().sum()) if not df.empty else 0

    return {
        "total_rows": total,
        "valid_rows": valid,
        "invalid_rows": int(invalid),
        "duplicate_rows": duplicates
    }


def get_dashboard_stats():
    """Dashboard API එකට අවශ්‍ය සියලුම Dynamic Live Data සකසා දෙයි"""
    stats = calculate_statistics()
    insights = get_historical_insights()
    quality = get_data_quality()

    total = quality["total_rows"]
    valid = quality["valid_rows"]
    q_score = (valid / total * 100) if total > 0 else 0

    if q_score >= 95:
        q_status = "🟢 High Quality Data"
    elif q_score >= 80:
        q_status = "🟡 Medium Quality Data"
    else:
        q_status = "🔴 Low Quality Data"

    return {
        "status": "success",
        "totalRounds": f"{stats['total_rounds']:,}",
        "averageCrash": f"{stats['average']:.2f}x",
        "highestCrash": f"{insights['highest']:.2f}x" if insights else "0.00x",
        "lowestCrash": f"{insights['lowest']:.2f}x" if insights else "0.00x",
        "distribution": {
            "below2": f"{stats['below_2']:.0f}%",
            "between25": f"{stats['between_2_5']:.0f}%",
            "between510": f"{stats['between_5_10']:.0f}%",
            "above10": f"{stats['above_10']:.0f}%"
        },
        "quality": {
            "score": f"{q_score:.0f}%",
            "status": q_status
        }
    }