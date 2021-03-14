#### Architecture Diagrams
- [Overall Architecture](https://app.diagrams.net/#G1u6movWe56NhjL4cRbYz5LUSHnYTF-qO1)
- [Data Sources Code](https://lucid.app/lucidchart/invitations/accept/47b854b5-905e-4b80-afd0-e7d3657a2dd8)
- [OnTheMarket Pipeline](https://drive.google.com/file/d/1LAIS6I_fxpi65tiTe7pjz1tlCuDe8lMU/view?usp=sharing)
- [Serverless Architectures with AWS Lambda](https://docs.aws.amazon.com/whitepapers/latest/serverless-architectures-lambda/code-repository-organization.html)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)


#### Cloud Services Providers
- [AWS Free Tier](https://aws.amazon.com/free)
- [GCP Free Tier](https://cloud.google.com/free)


#### Tutorials/Docs
- [Python Official Docs](https://docs.python.org/3/tutorial/)
- [Logging](https://www.youtube.com/watch?v=jxmzY9soFXg)
- [Data Engineering Roadmap](https://github.com/datastacktv/data-engineer-roadmap)
- [Data Engineering Learning Path](https://awesomedataengineering.com/)
	- [Database Design](https://www.youtube.com/watch?v=ztHopE5Wnpc)
- [7 Database Paradigms](https://www.youtube.com/watch?v=W2Z7fbCLSTw)


#### Which cloud service provider to pick? GCP VS AWS

**AWS**

- has many 12 month free tier products
- is more popular by a huge margin
- is preferred choice of many veteran developers

**GCP**

- has more always free products
- has bigquery
- Wei and Sabih are proficient at it


#### Setup project in dev mode

```
git clone https://github.com/sabih-h/creation-origins.git
cd creation-origins
pip install -e .
```

#### Data Sources

- [OnTheMarket](https://www.onthemarket.com/)
- [Price Paid data by gov.uk](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)


#### Helper datasets
- [London Postal Disticts](https://en.wikipedia.org/wiki/London_postal_district)
- [London stations gsheet](https://docs.google.com/spreadsheets/d/1t0u72RGnsKnsuOpH0XYOYnYBXA6g6E5g0oCDd1yJygc/edit#gid=1379759481)


#### Testing
`pytest -v`


#### Usage
```
import enova
enova.onthemarket.properties()


```
