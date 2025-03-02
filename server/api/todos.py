from flask import Flask, jsonify, request
from bson import ObjectId

from server.db import mongo
from server.application import app


class TodosService:
    collection = mongo.db.todos

    @classmethod
    def get_all_todos(cls):
        """Retrieve all tasks."""
        return [
            {
                "_id": str(todo["_id"]),
                "task": todo["task"],
                "completed": todo["completed"],
            }
            for todo in cls.collection.find()
        ]

    @classmethod
    def get_todo(cls, todo_id):
        """Retrieve a single task by ID."""
        todo = cls.collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            return {
                "_id": str(todo["_id"]),
                "task": todo["task"],
                "completed": todo["completed"],
            }
        return None

    @classmethod
    def create_todo(cls, task):
        """Create a new task."""
        todo_id = cls.collection.insert_one(
            {"task": task, "completed": False}
        ).inserted_id
        return str(todo_id)

    @classmethod
    def update_todo(cls, todo_id, update_data):
        """Update a task (mark as completed or change task)."""
        update_fields = {}

        if "task" in update_data:
            update_fields["task"] = update_data["task"]
        if "completed" in update_data:
            update_fields["completed"] = update_data["completed"]

        if not update_fields:
            return False

        result = cls.collection.update_one(
            {"_id": ObjectId(todo_id)}, {"$set": update_fields}
        )
        return result.modified_count > 0

    @classmethod
    def delete_todo(cls, todo_id):
        """Delete a task."""
        result = cls.collection.delete_one({"_id": ObjectId(todo_id)})
        return result.deleted_count > 0


class TodosAPI:
    """Class-based CRUD API for a To-Do App."""

    @staticmethod
    @app.route("/todos", methods=["GET"])
    def get_all_todos():
        """Retrieve all tasks."""
        todos = TodosService.get_all_todos()
        return jsonify(todos), 200

    @staticmethod
    @app.route("/todo/<string:todo_id>", methods=["GET"])
    def get_todo(todo_id):
        """Retrieve a single task by ID."""
        todo = TodosService.get_todo(todo_id)

        if todo:
            return jsonify(
                {
                    "_id": str(todo["_id"]),
                    "task": todo["task"],
                    "completed": todo["completed"],
                }
            ), 200

        return jsonify({"error": "Todo not found"}), 404

    @staticmethod
    @app.route("/todo", methods=["POST"])
    def create_todo():
        """Create a new task."""
        data = request.json

        if not data or "task" not in data:
            return jsonify({"error": "Task is required"}), 400

        todo_id = TodosService.create_todo(data["task"])

        return jsonify({"message": "Todo created", "id": str(todo_id)}), 201

    @staticmethod
    @app.route("/todo/<string:todo_id>", methods=["PUT"])
    def update_todo(todo_id):
        """Update a task (mark as completed or change task)."""
        data = request.json
        update_data = {}

        if "task" in data:
            update_data["task"] = data["task"]
        if "completed" in data:
            update_data["completed"] = data["completed"]

        if not update_data:
            return jsonify({"error": "No data to update"}), 400

        result = TodosService.update_todo(todo_id, update_data)

        if result.modified_count > 0:
            return jsonify({"message": "Todo updated"}), 200
        return jsonify({"error": "Todo not found or no changes made"}), 404

    @staticmethod
    @app.route("/todo/<string:todo_id>", methods=["DELETE"])
    def delete_todo(todo_id):
        """Delete a task."""
        result = TodosService.delete_todo(todo_id)

        if result.deleted_count > 0:
            return jsonify({"message": "Todo deleted"}), 200
        return jsonify({"error": "Todo not found"}), 404
