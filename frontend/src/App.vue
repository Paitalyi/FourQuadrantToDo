<template>
    <div class="quadrants">
        <div v-for="quadrant in quadrants" :key="quadrant.id" class="quadrant">
            <h2>{{ quadrant.title }}</h2>
            <ul>
                <li v-for="task in tasks[quadrant.id - 1]" :key="task.id">
                    <input type="checkbox" v-model="task.completed" @change="updateTask(task)">
                    <span :class="{ completed: task.completed }">{{ task.title }}</span>
                    <button @click="deleteTask(task.id)">删除</button>
                </li>
            </ul>
            <input v-model="newTaskTitles[quadrant.id - 1]" placeholder="添加新任务">
            <input v-model="newTaskDescriptions[quadrant.id - 1]" placeholder="添加任务描述">
            <button @click="addTask(quadrant, quadrant.id - 1)">添加</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const quadrants = [
    { id: 1, title: '重要且紧急', urgency: 1, importance: 1 },
    { id: 2, title: '重要不紧急', urgency: 0, importance: 1 },
    { id: 3, title: '紧急不重要', urgency: 1, importance: 0 },
    { id: 4, title: '不重要不紧急', urgency: 0, importance: 0 }
];

const newTaskTitles = ref(['', '', '', '']);
const newTaskDescriptions = ref(['', '', '', '']);
const tasks = ref([[],[],[],[]]);
const apiUrl = ref('http://localhost:5000/tasks');


const fetchTasks = async () => {
    try {
        const response = await axios.get(apiUrl.value);
        // 重置任务数组
        tasks.value = [[],[],[],[]];
        response.data.forEach(task => {
            const quadrantIndex = quadrants.findIndex(q => q.urgency === task.urgency && q.importance === task.importance);
            if (quadrantIndex !== -1) {
                tasks.value[quadrantIndex].push({ ...task, completed: false });
            }
        });
    } catch (error) {
        console.error('获取任务失败:', error);
    }
};

const addTask = async (quadrant, index) => {
    if (newTaskTitles.value[index].trim()) {
        try {
            const response = await axios.post(apiUrl.value, { 
                title: newTaskTitles.value[index], 
                description: newTaskDescriptions.value[index], 
                urgency: quadrant.urgency, 
                importance: quadrant.importance 
            });
            tasks.value[index].push({
              id: response.data.id,
              title: newTaskTitles.value[index],
              description: newTaskDescriptions.value[index],
              urgency: quadrant.urgency,
              importance: quadrant.importance,
              completed: false
            });
            newTaskTitles.value[index] = '';
            newTaskDescriptions.value[index] = '';
        } catch (error) {
            console.error('添加任务失败:', error);
        }
    }
};

const updateTask = async (task, quadrantIndex) => {
    try {
        await axios.put(`${apiUrl.value}/${task.id}`, task);
        // 更新对应象限的任务数据
        const index = tasks.value[quadrantIndex].findIndex(t => t.id === task.id);
        if (index !== -1) {
            tasks.value[quadrantIndex][index] = { ...task };
        }
    } catch (error) {
        console.error('更新任务失败:', error);
    }
};

const deleteTask = async (taskId, quadrantIndex) => {
    try {
        await axios.delete(`${apiUrl.value}/${taskId}`);
        tasks.value[quadrantIndex] = tasks.value[quadrantIndex].filter(task => task.id !== taskId);
    } catch (error) {
        console.error('删除任务失败:', error);
    }
};

onMounted(fetchTasks);
</script>

<style scoped>
.quadrants {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.quadrant {
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 8px;
}

.completed {
    text-decoration: line-through;
    color: #888;
}
</style>