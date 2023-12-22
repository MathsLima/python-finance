import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import yfinance as yf
import matplotlib
matplotlib.rcParams['figure.figsize'] = (16,8)

#https://www.youtube.com/watch?v=7rFsu48oBn8&list=PLCAhGm8nJ9CBn51o0x3j1p1LuMRqpeqCy&index=10

def consulta_bc(codigo_bc):
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json1'.format(codigo_bc)
    df = pd.read_json(url)
    df['data']  = pd.to_datetime(df['data'], dayfirst=True)
    df.set_index('data', inplace=True)
    return df

#para obter dados especificos mudar codigo de acordo com a plataforma bc
ipca = consulta_bc(433)   
igpm = consulta_bc(189)
selic_meta = consulta_bc(432)
reserva_total_diaria = consulta_bc(13621)

ibovespa =  yf.download("^BVSP", period="15y")['Adj Close']
ibovespa_retorno = ibovespa.pct_change()

inicio = '2015-01-01'

ibovespa_retorno_acumulado = (1 + ibovespa_retorno[ibovespa_retorno.index >= inicio]).cumprod()
ibovespa_retorno_acumulado.iloc[0] = 1

cdi = consulta_bc(12)

inicio = '2015-01-01'

cdi_acumulado = (1 + cdi[cdi.index >= inicio] / 100).cumprod()
cdi.iloc[0] = 1

fig, ax = plt.subplots()
ax.plot(ibovespa_retorno_acumulado)
ax.plot(cdi_acumulado)