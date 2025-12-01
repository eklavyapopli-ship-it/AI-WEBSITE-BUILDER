document.addEventListener('DOMContentLoaded', () => {
    const newTaskInput = document.getElementById('new-task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const startNowBtn = document.querySelector('.start-now-btn');
    const taskManagerSection = document.getElementById('task-manager-section');

    let tasks = [];
    let currentFilter = 'all'; // 'all', 'pending', 'completed'

    // --- Local Storage Functions ---
    const saveTasks = () => {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    };

    const loadTasks = () => {
        const storedTasks = localStorage.getItem('tasks');
        if (storedTasks) {
            tasks = JSON.parse(storedTasks);
        } else {
            // Pseudo data if no tasks are found
            tasks = [
                { id: Date.now(), text: 'Plan weekly team meeting', completed: false },
                { id: Date.now() + 1, text: 'Review Q3 financial reports', completed: false },
                { id: Date.now() + 2, text: 'Design new marketing banner', completed: true },
                { id: Date.now() + 3, text: 'Prepare presentation for client demo', completed: false }
            ];
            saveTasks();
        }
        renderTasks();
    };

    // --- Task Rendering Functions ---
    const createTaskElement = (task) => {
        const listItem = document.createElement('li');
        listItem.className = `task-item ${task.completed ? 'completed' : ''}`;
        listItem.setAttribute('data-id', task.id);

        const taskTextSpan = document.createElement('span');
        taskTextSpan.className = 'task-text';
        taskTextSpan.textContent = task.text;

        const taskActionsDiv = document.createElement('div');
        taskActionsDiv.className = 'task-actions';

        const completeBtn = document.createElement('button');
        completeBtn.className = `complete-btn ${task.completed ? 'completed-status' : 'pending-status'}`;
        completeBtn.innerHTML = task.completed ? '&#10003;' : '&#9711;'; // Checkmark / Circle
        completeBtn.title = task.completed ? 'Mark as Pending' : 'Mark as Complete';
        completeBtn.addEventListener('click', () => toggleTaskComplete(task.id));

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '&#10006;'; // X mark
        deleteBtn.title = 'Delete Task';
        deleteBtn.addEventListener('click', () => deleteTask(task.id));

        taskActionsDiv.appendChild(completeBtn);
        taskActionsDiv.appendChild(deleteBtn);

        listItem.appendChild(taskTextSpan);
        listItem.appendChild(taskActionsDiv);

        return listItem;
    };

    const renderTasks = () => {
        taskList.innerHTML = '';
        const filteredTasks = tasks.filter(task => {
            if (currentFilter === 'pending') return !task.completed;
            if (currentFilter === 'completed') return task.completed;
            return true;
        });

        filteredTasks.forEach(task => {
            const taskElement = createTaskElement(task);
            taskList.appendChild(taskElement);
            // Add entering animation class
            setTimeout(() => taskElement.classList.add('entered'), 10);
        });
    };

    // --- Task Actions ---
    const addTask = () => {
        const taskText = newTaskInput.value.trim();
        if (taskText) {
            const newTask = {
                id: Date.now(),
                text: taskText,
                completed: false
            };
            tasks.unshift(newTask); // Add to the beginning
            saveTasks();
            newTaskInput.value = '';
            renderTasks(); // Re-render to show new task with current filter

            // Smoothly scroll to the new task if it's visible
            const newElement = taskList.querySelector(`[data-id="${newTask.id}"]`);
            if (newElement) {
                newElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
    };

    const toggleTaskComplete = (id) => {
        tasks = tasks.map(task =>
            task.id === id ? { ...task, completed: !task.completed } : task
        );
        saveTasks();
        renderTasks();
    };

    const deleteTask = (id) => {
        const taskElement = taskList.querySelector(`[data-id="${id}"]`);
        if (taskElement) {
            taskElement.classList.add('deleting');
            taskElement.addEventListener('transitionend', () => {
                tasks = tasks.filter(task => task.id !== id);
                saveTasks();
                renderTasks();
            }, { once: true });
        }
    };

    // --- Event Listeners ---
    addTaskBtn.addEventListener('click', addTask);

    newTaskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    filterBtns.forEach(button => {
        button.addEventListener('click', () => {
            filterBtns.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentFilter = button.dataset.filter;
            renderTasks();
        });
    });

    startNowBtn.addEventListener('click', () => {
        taskManagerSection.scrollIntoView({
            behavior: 'smooth'
        });
    });

    // Initial load
    loadTasks();
});