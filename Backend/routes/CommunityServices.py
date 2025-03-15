from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/CommunityServices")

DB_PATH = "Servify.db"