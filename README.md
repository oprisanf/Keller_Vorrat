# Keller_Vorrat

Repository overview and quick links.

## Repository Diagram

The detailed repository diagram is in [REPO_INFO.md](REPO_INFO.md).

You can also view the diagram inline (Mermaid):

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
```

## Notes

- `REPO_INFO.md` contains the same diagram and extra context.
- If you'd like, I can render the Mermaid diagram to an image and add it here.
