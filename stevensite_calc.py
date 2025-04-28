#stevensite solubility product

#Given:
#logK = 25.45 @ 25C

#(Si_4.00, Mg_2.9, O_10, (OH)_2, Ca_0.1) + 6H+ + 4H20 = 4H4SiO4 + 2.9Mg++ +  0.1Ca++)

#Ksp = (H4SiO4 ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / ([H] ** 6)
#regarding the data set, Si is the limiting element for H4SiO4

#convertin [H+] to pH
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
def plot_logKsp_scatter():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/Data/Calculated Values/stevensite_combined_logKsp.csv')

    #standardize Sample_Type values
    df['Sample_Type'] = df['Sample_Type'].str.strip().str.lower()

    #define colors and custom labels for each sample type
    colors = {
        'pw_inactive': 'b',
        'pw_active': 'r',
        'boundary lake': 'g',
        'groundwater': 'y'
    }
    
    custom_labels = {
        'pw_inactive': 'Inactive (PW)',
        'pw_active': 'Active (PW)',
        'boundary lake': 'Boundary Lake',
        'groundwater': 'Groundwater'
    }

    plt.figure(figsize=(10, 6))

    #plot each group with custom labels
    for sample_type, group in df.groupby('Sample_Type'):
        label = custom_labels.get(sample_type, sample_type.title())  # Default to sample_type title if not found
        plt.scatter(group['Temperature (C)'], group['log_Ksp'],
                    label=label,
                    color=colors.get(sample_type))  

    plt.xlabel('Temperature (°C)')
    plt.ylabel('log(Ksp)')
    plt.title('log(Ksp) of Stevensite vs Temperature')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#box plot, comparing logKsp values to sample type
def plot_logKsp_boxplot():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/Data/Calculated Values/stevensite_combined_logKsp.csv')

    # Standardize Sample_Type values
    df['Sample_Type'] = df['Sample_Type'].str.strip()

    # Create boxplot with custom labels
    boxplot = df.boxplot(column='log_Ksp', by='Sample_Type', grid=False)
    plt.suptitle('')  # Suppress the default title
    plt.title('log(Ksp) of Stevensite by Sample Type')
    plt.xlabel('Sample Type')
    plt.ylabel('log(Ksp)')
    plt.xticks(rotation=45)

    #calculate and annotate median values


    medians = df.groupby('Sample_Type')['log_Ksp'].median()

    for i, sample_type in enumerate(medians.index):
        median_value = medians[sample_type]
        plt.text(
            i + 1.35,  # aligned with box position
            median_value - 1.0,  # slight offset downward
            f'{median_value:.2f}',
            ha='center',
            va='bottom',
            fontsize=8,  # not too large
            color='black',  # classic black text
            family='serif',  # serif font (like Times New Roman)
            style='italic'  # italic for a polished, academic feel
        )
    plt.legend(title='*Numbers indicate median values', loc='lower right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # grid only on y-axis
    plt.gca().set_facecolor('lightgrey')  # light grey background for the plot area
    plt.gcf().patch.set_facecolor('white')  # white background for the figure
    plt.gcf().set_size_inches(10, 6)  # set figure size
    plt.tight_layout()
    plt.show()


#plot_logKsp_scatter()
#plot_logKsp_boxplot()