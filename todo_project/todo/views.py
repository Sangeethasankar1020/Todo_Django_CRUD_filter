# todo/views.py

# views.py
from django.shortcuts import render, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
todos_collection = db['todos']

def home(request):
    tasks = list(todos_collection.find())

    # Convert ObjectId to string and separate date and time
    for task in tasks:
        task['id'] = str(task['_id'])  # Convert ObjectId to string
        # Assuming 'datetime' is a field that contains the date and time
        if 'datetime' in task:
            # Convert to datetime object
            dt = task['datetime']  # Change to the appropriate field name if needed
            if isinstance(dt, str):
                dt = datetime.fromisoformat(dt)  # Convert string to datetime if needed
            task['date'] = dt.date().isoformat()  # Extract date
            task['time'] = dt.time().isoformat()  # Extract time

    return render(request, 'home.html', {'tasks': tasks})


# Other views (add_task, update_task, delete_task) should remain unchanged

def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_datetime = request.POST.get('task_datetime')

        if task_name and task_datetime:
            # Insert task into MongoDB
            todos_collection.insert_one({
                'name': task_name,
                'datetime': task_datetime,
                'created_at': datetime.datetime.now()
            })
            return redirect('home')  # Redirect to home after adding
    return render(request, 'add_task.html')  # Render add task form if GET request

def update_task(request, task_id):
    task = todos_collection.find_one({'_id': ObjectId(task_id)})

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_datetime = request.POST.get('task_datetime')

        if task_name and task_datetime:
            # Update the task in MongoDB
            todos_collection.update_one(
                {'_id': ObjectId(task_id)},
                {'$set': {'name': task_name, 'datetime': task_datetime}}
            )
            return redirect('home')  # Redirect to home after updating

    return render(request, 'update_task.html', {'task': task})

def delete_task(request, task_id):
    # Delete the task from MongoDB
    todos_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect('home')  # Redirect to home after deleting

