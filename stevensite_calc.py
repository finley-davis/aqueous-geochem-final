#stevensite solubility product

#Given:
#logK = 25.45 @ 25C

#(Si_4.00, Mg_2.9, O_10, (OH)_2, Ca_0.1) + 6H+ + 4H20 = 4H4SiO4 + 2.9Mg++ +  0.1Ca++)

#Ksp = (H4SiO4 ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / ([H] ** 6)
#regarding the data set, Si is the limiting element for H4SiO4

#necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#load data
df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/Data/metadata_ioncomp.csv')


#extracting columns
Mg = df['Magnesium (Mg)'].to_numpy()
Ca = df['Calcium (Ca)'].to_numpy()
H4SiO4 = df['Silicon (Si)'].to_numpy()  # ssuming silicon column represents H4SiO4
df['Date'] = pd.to_datetime(df['Sample Date'], format='%m/%d/%y')
temp = df['Temperature (C)'].to_numpy()


#NOTE: Concentrations are in mmol/L

#fresh
def log_Ksp_stevensite_2014_SW():
    results = []
    for i in range(48, 62):  # specific rows for BL surface water
        pH = df['pH'].iloc[i]
        Mg = df['Magnesium (Mg)'].iloc[i]
        Ca = df['Calcium (Ca)'].iloc[i]
        Si = df['Silicon (Si)'].iloc[i]  # assuming Si = H4SiO4
        temp = df['Temperature (C)'].iloc[i]
        date = df['Date'].iloc[i]

        H = 10 ** (-pH)
        Ksp = (Si ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / (H ** 6)
        log_ksp = np.log10(Ksp)

        results.append({'Date': date, 'Temperature (C)': temp, 'log_Ksp': log_ksp, 'pH': pH})

    return pd.DataFrame(results)


    #output this into csv file

#saline
def log_Ksp_stevensite_2014_PW_Inactive():
    results = []

    for i in range(5, 21):
        pH = df['pH'].iloc[i]
        Mg = df['Magnesium (Mg)'].iloc[i]
        Ca = df['Calcium (Ca)'].iloc[i]
        Si = df['Silicon (Si)'].iloc[i]
        temp = df['Temperature (C)'].iloc[i]
        H = 10 ** -pH

        Ksp = (Si ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / (H ** 6)
        log_ksp = np.log10(Ksp)

        date = df['Date'].iloc[i]
        results.append({'Date': date, 'Temperature (C)': temp, 'log_Ksp': log_ksp, 'pH': pH})

    return pd.DataFrame(results)

#saline
def log_Ksp_stevensite_2014_PW_Active():
    results = []

    for i in range(23, 43):
        pH = df['pH'].iloc[i]
        Mg = df['Magnesium (Mg)'].iloc[i]
        Ca = df['Calcium (Ca)'].iloc[i]
        Si = df['Silicon (Si)'].iloc[i]
        temp = df['Temperature (C)'].iloc[i]
        H = 10 ** -pH

        Ksp = (Si ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / (H ** 6)
        log_ksp = np.log10(Ksp)

        date = df['Date'].iloc[i]
        results.append({'Date': date, 'Temperature (C)': temp, 'log_Ksp': log_ksp, 'pH': pH})

    return pd.DataFrame(results)

#brackish
def log_Ksp_stevensite_2014_GW():
    results = []

    for i in range(3, 5):
        pH = df['pH'].iloc[i]
        Mg = df['Magnesium (Mg)'].iloc[i]
        Ca = df['Calcium (Ca)'].iloc[i]
        Si = df['Silicon (Si)'].iloc[i]
        temp = df['Temperature (C)'].iloc[i]
        H = 10 ** -pH

        Ksp = (Si ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / (H ** 6)
        log_ksp = np.log10(Ksp)

        date = df['Date'].iloc[i]
        results.append({'Date': date, 'Temperature (C)': temp, 'log_Ksp': log_ksp, 'pH': pH})

    return pd.DataFrame(results)

#run functions
def run_above_functions():
    SW = log_Ksp_stevensite_2014_SW()
    SW['Sample_Type'] = 'Surface Water'

    PW_Inactive = log_Ksp_stevensite_2014_PW_Inactive()
    PW_Inactive['Sample_Type'] = 'Inactive Pore Water'

    PW_Active = log_Ksp_stevensite_2014_PW_Active()
    PW_Active['Sample_Type'] = 'Active Pore Water'

    GW = log_Ksp_stevensite_2014_GW()
    GW['Sample_Type'] = 'Groundwater'

    #combine into one DataFrame
    combined_df = pd.concat([SW, PW_Inactive, PW_Active, GW], ignore_index=True)

    #save to CSV
    combined_df.to_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/Data/stevensite_combined_logKsp.csv', index=False)

#scatter plot, comparing logKsp values to temperature
def plot_SI_scatter():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/github/CSV Data/Stevensite_SI_phrqc.csv')

    df['Sample Type'] = df['Sample Type'].str.strip()

    colors = {
        'Inactive Pore Water': 'b',
        'Active Pore Water': 'r',
        'Surface Water': 'g',
        'Groundwater': 'y'
    }

    custom_labels = {
        'Inactive Pore Water': 'Inactive (PW)',
        'Active Pore Water': 'Active (PW)',
        'Surface Water': 'Boundary Lake',
        'Groundwater': 'Groundwater'
    }

    plt.figure(figsize=(10, 6))


    for sample_type, group in df.groupby('Sample Type'):
        label = custom_labels.get(sample_type, sample_type)
        plt.scatter([sample_type] * len(group), group['si_Sepiolite'],
                    label=label,
                    color=colors.get(sample_type, 'gray'), 
                    edgecolor='k')

    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, label='Equilibrium')
    plt.xlabel('Sample Type', fontweight='bold')
    plt.ylabel('SI (Sepiolite)', fontweight='bold')
    plt.title('SI of Sepiolite by Sample Type', fontweight='bold')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#box plot, comparing logKsp values to sample type
def plot_SI_boxplot():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper'
    '/github/CSV Data/Stevensite_SI_phrqc.csv')

    df['Sample Type'] = df['Location ID'].str.strip()

    # Filter out rows where 'Location ID' is 'Undisclosed Porewater'
    df = df[df['Sample Type'] != 'Undisclosed Porewater']

    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(data=df, x='Sample Type', y='si_Sepiolite', palette='pastel')
    
    medians = df.groupby('Sample Type')['si_Sepiolite'].median()
    xticks = ax.get_xticks()
    
    for tick, label in zip(xticks, ax.get_xticklabels()):
        sample_type = label.get_text()
        median_value = medians[sample_type]
        ax.text(
            tick, median_value - 0.4,
            f'{median_value:.2f}',
            ha='center',
            va='bottom',
            fontsize=8,
            color='black',
            family='serif',
            style='italic'
        )

    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, label='Equilibrium')
    plt.title('SI of Sepiolite by Sample Type', fontweight='bold')
    plt.ylabel('SI (Sepiolite)', fontweight='bold')
    plt.xlabel('Sample Type', fontweight='bold')
    plt.xticks(rotation=45)
    plt.legend(loc='lower right', title='*Median values shown', fontsize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_facecolor('lightgrey')
    plt.gcf().patch.set_facecolor('white')
    plt.tight_layout()
    plt.show()


#plot_SI_scatter()
plot_SI_boxplot()