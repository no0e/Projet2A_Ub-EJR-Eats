
```mermaid
---
title: Quick Architecture overview
---
    graph LR
    USR1((Drivers))
    USR2((Admin))
    USR3((Customers))
    DB[("fa:fa-database App Database \n (PostgreSQL)" )]
    INT(fa:fa-python Interface Layer / \n WebService)
    DAO(fa:fa-python DAO)
    SVC(fa:fa-python Service / \n Controllers )
    MDB[(fa:fa-database Google Map)]
    MDBAPI(Google Map API)

    USR1 <--> INT
    USR2 <--> INT
    USR3 <--> INT
        subgraph Python app 
            API<-->SVC<-->DAO
            subgraph INT[fa:fa-python Interface ]
                API(fa:fa-lock API)
            end
            subgraph SVC [fa:fa-python Service / Controllers]
                ORD(fa:fa-lock Order Service)
                MEN(fa:fa-film Menus Service)
                AUT(fa:fa-user Authentication Service)
                MAP(fa:fa-film Map Service)
            end
        end

    DAO<--->DB
    MDBAPI <--> MDB
    SVC <--> MDBAPI

  %% ==== Styles personnalisés ====
    classDef orange fill:#FF8C00,stroke:#333,stroke-width:2px,color:#fff;
    classDef lightorange fill:#FFB65C,stroke:#333,stroke-width:2px,color:#000;
    classDef teal fill:#1CAABD,stroke:#333,stroke-width:2px,color:#fff;

    %% Attribution des couleurs
    class USR1,USR2,USR3 orange
    class DB,MDB teal
    class API,DAO,SVC,ORD,MEN,AUT,MAP, MDB lightorange
```
