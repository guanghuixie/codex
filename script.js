const STORAGE_KEY = "codex.todo-list.todos";
const FILTERS = new Set(["all", "active", "completed"]);

function createId() {
  if (globalThis.crypto?.randomUUID) {
    return globalThis.crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function addTodo(todos, text) {
  const value = text.trim();

  if (!value) {
    throw new Error("待办事项不能为空");
  }

  return [
    ...todos,
    {
      id: createId(),
      text: value,
      completed: false,
      createdAt: new Date().toISOString(),
    },
  ];
}

function toggleTodo(todos, id) {
  return todos.map((todo) =>
    todo.id === id ? { ...todo, completed: !todo.completed } : todo,
  );
}

function deleteTodo(todos, id) {
  return todos.filter((todo) => todo.id !== id);
}

function clearCompleted(todos) {
  return todos.filter((todo) => !todo.completed);
}

function filterTodos(todos, filter) {
  if (filter === "active") {
    return todos.filter((todo) => !todo.completed);
  }

  if (filter === "completed") {
    return todos.filter((todo) => todo.completed);
  }

  return todos;
}

function getRemainingCount(todos) {
  return todos.filter((todo) => !todo.completed).length;
}

function loadTodos() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveTodos(todos) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

function createTodoItem(todo) {
  const item = document.createElement("li");
  item.className = `todo-item${todo.completed ? " completed" : ""}`;
  item.dataset.id = todo.id;

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = todo.completed;
  checkbox.setAttribute("aria-label", `${todo.completed ? "取消完成" : "完成"} ${todo.text}`);

  const text = document.createElement("span");
  text.className = "todo-text";
  text.textContent = todo.text;

  const remove = document.createElement("button");
  remove.className = "delete-button";
  remove.type = "button";
  remove.textContent = "删";
  remove.setAttribute("aria-label", `删除 ${todo.text}`);

  item.append(checkbox, text, remove);
  return item;
}

function mountTodoApp() {
  const form = document.querySelector("#todo-form");
  const input = document.querySelector("#todo-input");
  const error = document.querySelector("#todo-error");
  const list = document.querySelector("#todo-list");
  const count = document.querySelector("#todo-count");
  const clearButton = document.querySelector("#clear-completed");
  const filterButtons = [...document.querySelectorAll(".filter-button")];

  let todos = loadTodos();
  let currentFilter = "all";

  function setError(message = "") {
    error.textContent = message;
  }

  function commit(nextTodos) {
    todos = nextTodos;
    saveTodos(todos);
    render();
  }

  function render() {
    const visibleTodos = filterTodos(todos, currentFilter);
    list.innerHTML = "";

    if (visibleTodos.length === 0) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      empty.textContent = currentFilter === "all" ? "还没有待办事项" : "当前筛选下没有任务";
      list.append(empty);
    } else {
      const fragment = document.createDocumentFragment();
      visibleTodos.forEach((todo) => fragment.append(createTodoItem(todo)));
      list.append(fragment);
    }

    const remaining = getRemainingCount(todos);
    count.textContent = `${remaining} 项未完成`;
    clearButton.disabled = !todos.some((todo) => todo.completed);

    filterButtons.forEach((button) => {
      const active = button.dataset.filter === currentFilter;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    try {
      commit(addTodo(todos, input.value));
      input.value = "";
      input.focus();
      setError();
    } catch (err) {
      setError(err.message);
    }
  });

  list.addEventListener("change", (event) => {
    const checkbox = event.target.closest('input[type="checkbox"]');
    const item = event.target.closest(".todo-item");

    if (!checkbox || !item) {
      return;
    }

    commit(toggleTodo(todos, item.dataset.id));
  });

  list.addEventListener("click", (event) => {
    const button = event.target.closest(".delete-button");
    const item = event.target.closest(".todo-item");

    if (!button || !item) {
      return;
    }

    commit(deleteTodo(todos, item.dataset.id));
  });

  clearButton.addEventListener("click", () => {
    commit(clearCompleted(todos));
  });

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const nextFilter = button.dataset.filter;
      currentFilter = FILTERS.has(nextFilter) ? nextFilter : "all";
      render();
    });
  });

  render();
}

globalThis.TodoApp = {
  addTodo,
  toggleTodo,
  deleteTodo,
  clearCompleted,
  filterTodos,
  getRemainingCount,
};

if (typeof document !== "undefined") {
  mountTodoApp();
}
