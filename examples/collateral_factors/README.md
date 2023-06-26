# Collateral Factor - Using Postgres Data

This example illustrates a few things:

1. Connecting LangChain to your own data sources
2. Using Pandas data frames to feed LangChain private data
3. Using that customized model to get predictions

This example connects to a Postgres database to load historical collateral
factor data for issuing crypto loans. Then it uses that data in addition to more recent pricing, volume,
etc. data to predict new collateral factors
