"""
PLACEMENT ANALYTICS SYSTEM — Python EDA + Visualizations
Author: Yathendra Kumar Pasumarthi
Tools: Pandas, NumPy, Matplotlib, Seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# LOAD DATA
df = pd.read_csv('dataset/Sample.csv')
df.columns = df.columns.str.strip()

# DATA CLEANING
print("=" * 55)
print("  PLACEMENT ANALYTICS SYSTEM")
print("=" * 55)
print(f"\nTotal Records     : {len(df)}")
print(f"Missing Values    : {df.isnull().sum().sum()}")
print(f"Duplicate Records : {df.duplicated().sum()}")
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['Placed'] = df['Placement_Status'].apply(lambda x: 1 if x == 'Placed' else 0)
placed_df     = df[df['Placement_Status'] == 'Placed']
not_placed_df = df[df['Placement_Status'] == 'Not Placed']

total         = len(df)
placed        = len(placed_df)
not_placed    = len(not_placed_df)
placement_pct = round(placed / total * 100, 2)
avg_cgpa_p    = round(placed_df['Cgpa'].mean(), 2)
avg_cgpa_np   = round(not_placed_df['Cgpa'].mean(), 2)

print(f"\nTotal Students: {total}")
print(f"Placed: {placed} ({placement_pct}%)")
print(f"Not Placed: {not_placed}")
print(f"Avg CGPA Placed: {avg_cgpa_p} | Not Placed: {avg_cgpa_np}")

stream_analysis = df.groupby('Stream').apply(
    lambda x: pd.Series({
        'Total': len(x),
        'Placed': x['Placed'].sum(),
        'Placement_%': round(x['Placed'].sum() / len(x) * 100, 1),
    })
).reset_index().sort_values('Placement_%', ascending=False)

factors = ['Internship', 'Training', 'Backlog', 'Innovative_Project', 'Technical_Course']
print("\nFACTOR IMPACT:")
for factor in factors:
    yes = round(df[df[factor]=='Yes']['Placed'].mean()*100, 1)
    no  = round(df[df[factor]=='No']['Placed'].mean()*100, 1)
    print(f"  {factor:<25} Yes={yes}%  No={no}%")

bins   = [0, 6, 7, 8, 9, 10]
labels = ['<6.0', '6-7', '7-8', '8-9', '9-10']
df['CGPA_Range'] = pd.cut(df['Cgpa'], bins=bins, labels=labels)
df['Gender_Label'] = df['Gender'].map({'M':'Male','F':'Female'})

# VISUALIZATIONS
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(20, 24))
fig.suptitle('Placement Analytics Dashboard\nAuthor: Yathendra Kumar Pasumarthi',
             fontsize=20, fontweight='bold', y=0.98)

# Chart 1 KPI Cards
ax0 = fig.add_subplot(4,3,1); ax0.axis('off')
kpis = [("Total Students",str(total)),("Placement Rate",f"{placement_pct}%"),
        ("Avg CGPA Placed",str(avg_cgpa_p)),("Avg CGPA Not Placed",str(avg_cgpa_np))]
for idx,(label,val) in enumerate(kpis):
    y=0.85-idx*0.21
    ax0.text(0.5,y,val,ha='center',fontsize=22,fontweight='bold',color='#1F4E79',transform=ax0.transAxes)
    ax0.text(0.5,y-0.09,label,ha='center',fontsize=9,color='gray',transform=ax0.transAxes)
ax0.set_title('Key Metrics',fontweight='bold',fontsize=12)

# Chart 2 Pie
ax1=fig.add_subplot(4,3,2)
s=df['Placement_Status'].value_counts()
ax1.pie(s,labels=s.index,autopct='%1.1f%%',colors=['#2E75B6','#E74C3C'],startangle=90,textprops={'fontsize':11})
ax1.set_title('Placement Status',fontweight='bold')

# Chart 3 Gender
ax2=fig.add_subplot(4,3,3)
df.groupby(['Gender_Label','Placement_Status']).size().unstack(fill_value=0).plot(kind='bar',ax=ax2,color=['#E74C3C','#2E75B6'],edgecolor='white',width=0.5)
ax2.set_title('Gender vs Placement',fontweight='bold'); ax2.set_xlabel(''); ax2.tick_params(axis='x',rotation=0)

# Chart 4 Top Streams
ax3=fig.add_subplot(4,3,4)
ts=stream_analysis.head(8).sort_values('Placement_%')
bars=ax3.barh(ts['Stream'],ts['Placement_%'],color='#2E75B6',edgecolor='white')
ax3.set_title('Top Streams by Placement %',fontweight='bold'); ax3.set_xlabel('Placement %')
for bar,val in zip(bars,ts['Placement_%']):
    ax3.text(bar.get_width()+0.5,bar.get_y()+bar.get_height()/2,f'{val}%',va='center',fontsize=9,fontweight='bold')
ax3.set_xlim(0,115)

# Chart 5 CGPA Histogram
ax4=fig.add_subplot(4,3,5)
placed_df['Cgpa'].plot(kind='hist',bins=15,alpha=0.7,color='#2E75B6',label='Placed',ax=ax4)
not_placed_df['Cgpa'].plot(kind='hist',bins=15,alpha=0.7,color='#E74C3C',label='Not Placed',ax=ax4)
ax4.set_title('CGPA Distribution',fontweight='bold'); ax4.set_xlabel('CGPA'); ax4.legend()

# Chart 6 CGPA Range
ax5=fig.add_subplot(4,3,6)
cp=df.groupby('CGPA_Range',observed=True)['Placed'].mean()*100
sns.barplot(x=cp.index.astype(str),y=cp.values,palette='Blues',ax=ax5)
ax5.set_title('CGPA Range vs Placement %',fontweight='bold'); ax5.set_xlabel('CGPA Range'); ax5.set_ylabel('Placement %')
for i,v in enumerate(cp.values): ax5.text(i,v+1,f'{v:.1f}%',ha='center',fontsize=9,fontweight='bold')

# Chart 7 Factor Impact
ax6=fig.add_subplot(4,3,7)
fl=['Internship','Training','Backlog','Innov.Project','Tech Course']
yr,nr=[],[]
for factor in factors:
    yr.append(round(df[df[factor]=='Yes']['Placed'].mean()*100,1))
    nr.append(round(df[df[factor]=='No']['Placed'].mean()*100,1))
x=np.arange(len(fl)); w=0.35
ax6.bar(x-w/2,yr,w,label='Yes',color='#2E75B6',edgecolor='white')
ax6.bar(x+w/2,nr,w,label='No',color='#E74C3C',edgecolor='white')
ax6.set_xticks(x); ax6.set_xticklabels(fl,fontsize=8,rotation=15,ha='right')
ax6.set_ylabel('Placement %'); ax6.set_title('Factor Impact',fontweight='bold'); ax6.legend(fontsize=9)

# Chart 8 Communication
ax7=fig.add_subplot(4,3,8)
cp2=df.groupby('Communication_Score')['Placed'].mean()*100
sns.barplot(x=cp2.index,y=cp2.values,palette='Greens',ax=ax7)
ax7.set_title('Communication Score vs Placement',fontweight='bold'); ax7.set_xlabel('Score (1-5)'); ax7.set_ylabel('Placement %')
for i,v in enumerate(cp2.values): ax7.text(i,v+1,f'{v:.1f}%',ha='center',fontsize=9,fontweight='bold')

# Chart 9 10th Marks
ax8=fig.add_subplot(4,3,9)
placed_df['Marks_10th'].plot(kind='hist',bins=15,alpha=0.7,color='#2E75B6',label='Placed',ax=ax8)
not_placed_df['Marks_10th'].plot(kind='hist',bins=15,alpha=0.7,color='#E74C3C',label='Not Placed',ax=ax8)
ax8.set_title('10th Marks Distribution',fontweight='bold'); ax8.set_xlabel('Marks (%)'); ax8.legend()

# Chart 10 12th Marks
ax9=fig.add_subplot(4,3,10)
placed_df['Marks_12th'].plot(kind='hist',bins=15,alpha=0.7,color='#2E75B6',label='Placed',ax=ax9)
not_placed_df['Marks_12th'].plot(kind='hist',bins=15,alpha=0.7,color='#E74C3C',label='Not Placed',ax=ax9)
ax9.set_title('12th Marks Distribution',fontweight='bold'); ax9.set_xlabel('Marks (%)'); ax9.legend()

# Chart 11 Backlog
ax10=fig.add_subplot(4,3,11)
df.groupby(['Backlog','Placement_Status']).size().unstack(fill_value=0).plot(kind='bar',ax=ax10,color=['#E74C3C','#2E75B6'],edgecolor='white',width=0.5)
ax10.set_title('Backlog Impact',fontweight='bold'); ax10.set_xlabel('Has Backlog?'); ax10.tick_params(axis='x',rotation=0)

# Chart 12 Heatmap
ax11=fig.add_subplot(4,3,12)
sns.heatmap(df[['Cgpa','Marks_10th','Marks_12th','Communication_Score','Placed']].corr(),
    annot=True,fmt='.2f',cmap='Blues',ax=ax11,linewidths=0.5,annot_kws={'size':9})
ax11.set_title('Correlation Heatmap',fontweight='bold'); ax11.tick_params(axis='x',rotation=45)

plt.tight_layout(rect=[0,0,1,0.97])
plt.savefig('charts/placement_dashboard.png',dpi=150,bbox_inches='tight')
plt.close()
print("\n✅ Dashboard saved: charts/placement_dashboard.png")
print("✅ EDA Complete!")
