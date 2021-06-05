import requests
from sqlalchemy import Column, String, create_engine, event, DDL, Integer, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

conn_string = "postgres://user:password@host:port/db"
db = create_engine(conn_string, echo=True)
Base = declarative_base()

event.listen(
    Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS orm_example_countries")
)


class Country(Base):
    __tablename__ = "country"
    __table_args__ = {"schema": "orm_example_countries"}

    country_tlc = Column(String(3), primary_key=True)
    name = Column(String(150))
    capital = Column(String(30))
    population = Column(Integer)
    native_name = Column(String(150))

    country_currencies = relationship("CountryCurrency", cascade="all, delete-orphan", backref="country")
    currencies = association_proxy('country_currencies', 'currency')

    country_languages = relationship("CountryLanguage", cascade="all, delete-orphan", backref="country")
    languages = association_proxy('country_languages', 'language')


class Currency(Base):
    __tablename__ = "currency"
    __table_args__ = {"schema": "orm_example_countries"}

    code = Column(String(6), primary_key=True, )
    name = Column(String)
    symbol = Column(String(50))

    def __init__(self, code=None, name=None, symbol=None):
        self.code = code
        self.name = name
        self.symbol = symbol


class Language(Base):
    __tablename__ = "language"
    __table_args__ = {"schema": "orm_example_countries"}

    iso639_2 = Column(String(3), primary_key=True, )
    iso639_1 = Column(String(2))
    name = Column(String)
    native_name = Column(String(50))

    def __init__(self, iso639_1, iso639_2, name, native_name):
        self.iso639_1 = iso639_1
        self.iso639_2 = iso639_2
        self.name = name
        self.native_name = native_name


class CountryCurrency(Base):
    __tablename__ = "country_currency"
    __table_args__ = {"schema": "orm_example_countries"}

    country_tlc = Column(String, ForeignKey(Country.country_tlc), primary_key=True)
    currency_code = Column(String, ForeignKey(Currency.code), primary_key=True)

    currency = relationship("Currency")

    def __init__(self, currency_to_store):
        self.currency_code = currency_to_store.code


class CountryLanguage(Base):
    __tablename__ = "country_language"
    __table_args__ = {"schema": "orm_example_countries"}

    country_tlc = Column(String, ForeignKey(Country.country_tlc), primary_key=True)
    language_id = Column(String, ForeignKey(Language.iso639_2), primary_key=True)

    language = relationship("Language")

    def __init__(self, language_to_store):
        self.language_id = language_to_store.iso639_2


Session = sessionmaker(db)
session = Session()

Base.metadata.drop_all(db)
Base.metadata.create_all(db)

response = requests.get("https://restcountries.eu/rest/v2/all")

countries_data = response.json()

for country in countries_data:

    country_to_save = Country(
        country_tlc=country.get("alpha3Code"),
        name=country.get("name"),
        capital=country.get("capital"),
        population=country.get("population"),
        native_name=country.get("nativeName"),
    )

    currencies_from_api = country.get("currencies")
    for currency in currencies_from_api:
        currency_to_save = Currency(
            code=currency.get("code"),
            name=currency.get("name"),
            symbol=currency.get("symbol"),
        )

        if currency_to_save.code is None:
            continue

        currency_exists = session.query(Currency).filter_by(code=currency_to_save.code).first()
        if currency_exists:
            country_to_save.currencies.append(currency_to_save)
            continue
        else:
            session.add(currency_to_save)
            session.commit()
            country_to_save.currencies.append(currency_to_save)

    languages_from_api = country.get("languages")
    for language in languages_from_api:
        language_to_save = Language(
            iso639_1=language.get("iso639_1"),
            iso639_2=language.get("iso639_2"),
            name=language.get("name"),
            native_name=language.get("nativeName")
        )
        language_exists = session.query(Language).filter_by(iso639_2=language_to_save.iso639_2).first()
        if language_exists:
            country_to_save.languages.append(language_to_save)
            continue
        else:
            session.add(language_to_save)
            session.commit()
            country_to_save.languages.append(language_to_save)

    session.add(country_to_save)
    session.commit()
