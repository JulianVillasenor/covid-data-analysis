## Data description

- `ID_REGISTRO`: Número identificador del caso.
- `ENTIDAD_RES`: Identifica la entidad de residencia del paciente. 
- `MUNICIPIO_RES`: Identifica el municipio de residencia del paciente.
- `SEXO`: Identifica al sexo del paciente.
- `EDAD`: Identifica la edad del paciente.
- `TIPO_PACIENTE`: Identifica el tipo de atención que recibió el paciente en la unidad. Se denomina como ambulatorio si regresó a su casa o se denomina como hospitalizado si fue ingresado a hospitalización.
- `FECHA_SINTOMAS`: Idenitifica la fecha en que inició la sintomatología del paciente.
- `FECHA_DEF`: Identifica la fecha en que el paciente falleció.
- `DIABETES`: Identifica si el paciente tiene un diagnóstico de diabetes. 
- `OBESIDAD`: Identifica si el paciente tiene diagnóstico de obesidad.
- `HIPERTENSION`: Identifica si el paciente tiene un diagnóstico de hipertensión. 
- `TABAQUISMO`: Identifica si el paciente tiene hábito de tabaquismo.

### Data 2020 (df_2020)

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1563135 entries, 0 to 1563134
Data columns (total 12 columns):
 #   Column          Non-Null Count    Dtype 
---  ------          --------------    ----- 
 0   ID_REGISTRO     1563135 non-null  object
 1   ENTIDAD_RES     1563135 non-null  int64 
 2   MUNICIPIO_RES   1563135 non-null  int64 
 3   SEXO            1563135 non-null  int64 
 4   EDAD            1563135 non-null  int64 
 5   TIPO_PACIENTE   1563135 non-null  int64 
 6   FECHA_SINTOMAS  1563135 non-null  object
 7   FECHA_DEF       164384 non-null   object
 8   DIABETES        1563135 non-null  int64 
 9   OBESIDAD        1563135 non-null  int64 
 10  HIPERTENSION    1563135 non-null  int64 
 11  TABAQUISMO      1563135 non-null  int64 
dtypes: int64(9), object(3)
memory usage: 143.1+ MB
```

### Data 2021 (df_2021)

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2526649 entries, 0 to 2526648
Data columns (total 12 columns):
 #   Column          Non-Null Count    Dtype 
---  ------          --------------    ----- 
 0   ID_REGISTRO     2526649 non-null  object
 1   ENTIDAD_RES     2526649 non-null  int64 
 2   MUNICIPIO_RES   2526649 non-null  int64 
 3   SEXO            2526649 non-null  int64 
 4   EDAD            2526649 non-null  int64 
 5   TIPO_PACIENTE   2526649 non-null  int64 
 6   FECHA_SINTOMAS  2526649 non-null  object
 7   FECHA_DEF       141499 non-null   object
 8   DIABETES        2526649 non-null  int64 
 9   OBESIDAD        2526649 non-null  int64 
 10  HIPERTENSION    2526649 non-null  int64 
 11  TABAQUISMO      2526649 non-null  int64 
dtypes: int64(9), object(3)
memory usage: 231.3+ MB
```

### Data 2022 (df_2022)

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3195409 entries, 0 to 3195408
Data columns (total 12 columns):
 #   Column          Non-Null Count    Dtype 
---  ------          --------------    ----- 
 0   ID_REGISTRO     3195409 non-null  object
 1   ENTIDAD_RES     3195409 non-null  int64 
 2   MUNICIPIO_RES   3195409 non-null  int64 
 3   SEXO            3195409 non-null  int64 
 4   EDAD            3195409 non-null  int64 
 5   TIPO_PACIENTE   3195409 non-null  int64 
 6   FECHA_SINTOMAS  3195409 non-null  object
 7   FECHA_DEF       26108 non-null    object
 8   DIABETES        3195409 non-null  int64 
 9   OBESIDAD        3195409 non-null  int64 
 10  HIPERTENSION    3195409 non-null  int64 
 11  TABAQUISMO      3195409 non-null  int64 
dtypes: int64(9), object(3)
memory usage: 292.5+ MB
```

### Data consolidated (df)

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7285193 entries, 0 to 7285192
Data columns (total 12 columns):
 #   Column          Non-Null Count    Dtype 
---  ------          --------------    ----- 
 0   ID_REGISTRO     7285193 non-null  object
 1   ENTIDAD_RES     7285193 non-null  int64 
 2   MUNICIPIO_RES   7285193 non-null  int64 
 3   SEXO            7285193 non-null  int64 
 4   EDAD            7285193 non-null  int64 
 5   TIPO_PACIENTE   7285193 non-null  int64 
 6   FECHA_SINTOMAS  7285193 non-null  object
 7   FECHA_DEF       331991 non-null   object
 8   DIABETES        7285193 non-null  int64 
 9   OBESIDAD        7285193 non-null  int64 
 10  HIPERTENSION    7285193 non-null  int64 
 11  TABAQUISMO      7285193 non-null  int64 
dtypes: int64(9), object(3)
memory usage: 667.0+ MB
```