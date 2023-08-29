from config.supabase_config import * 
from flask import Flask, current_app, request, Blueprint, jsonify
from flask_cors import CORS, cross_origin