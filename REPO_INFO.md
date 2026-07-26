# Repository Overview

This file provides a high-level diagram of the repository structure and relationships using a Mermaid flowchart.

```mermaid
flowchart TB
  subgraph Root
    main[main_app.py]
    dockerfile[Dockerfile]
    compose[docker-compose.yml]
    streamlit[DockerStreamlit/]
    req1[requirments.txt]
    req2[requirments_streamlit.txt]
    prometheus[prometheus_data/]
    src[src/]
  end

  subgraph prometheus_data [prometheus_data/]
    promy[prometheus.yml]
  end

  subgraph src_folder [src/]
    s_init[__init__.py]
    s_crud[crud.py]
    s_db[database.py]
    s_models[models.py]
    s_api[new_api.py]
    s_schemas[schemas.py]
    s_utils[utils/]
  end

  subgraph src_utils [src/utils]
    u_photo[photo_scan.py]
    u_utils[utils.py]
  end

  %% relationships
  main -->|imports / uses| src
  main -->|runs in| streamlit
  compose -->|builds| dockerfile
  compose -->|runs| main
  dockerfile -->|image for| streamlit
  prometheus --> promy
  src --> s_init
  src --> s_crud
  src --> s_db
  src --> s_models
  src --> s_api
  src --> s_schemas
  src --> s_utils
  s_utils --> u_photo
  s_utils --> u_utils

  classDef file fill:#f9f,stroke:#333,stroke-width:1px;
  class main,dockerfile,compose,streamlit,req1,req2,prometheus,src file;

  %% Legend
  %% Note: node names map to filesystem items in the repository root and src/
```

Legend:
- main_app.py — application entrypoint
- Dockerfile, docker-compose.yml — containerization
- DockerStreamlit — folder for Streamlit Docker configuration
- `requirments*.txt` — Python dependencies (note spelling preserved from repo)
- prometheus_data/ — monitoring config
- src/ — application package and modules

If you'd like, I can also render this Mermaid diagram to PNG/SVG, or add it to the README.
