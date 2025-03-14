from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/BookmarkedServices")

DB_PATH = "Servify.db"