# Maintenance Guide - Bakery Data & Ratings

This guide explains how to manually update bakery information, especially ratings, to keep the service up-to-date with Kakao Map.

## 1. Updating Curated Data

The core bakeries are stored in the `_RAW_BAKERIES` list within `app/data.py`.

### Steps:
1.  Open `app/data.py`.
2.  Find the `_RAW_BAKERIES` list.
3.  Locate the bakery and update the `"rating"` or `"kakao_id"` field.

## 2. Default Ratings
Public data bakeries default to **3.5** in the `_load_public_bakeries` function in `app/data.py`.

## 3. Real-time Limitations
Currently, ratings are static to ensure fast performance and avoid API costs. Manual updates are recommended for the most accurate experience.
