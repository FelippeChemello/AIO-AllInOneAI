# AIO

## Description

This is a proxy server that unifies the API of OpenAI, Bing, Bard, POE and Claude.
Under the hood, it uses the following reverse engineering projects:

- [EdgeGPT](https://github.com/acheong08/EdgeGPT)
- [BardAPI](https://github.com/dsdanielpark/Bard-API)

## Running

```bash
uvicorn app:app --reload
```