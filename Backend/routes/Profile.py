from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/Profile")

DB_PATH = "Servify.db"