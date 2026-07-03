import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const htmlPath = path.join(root, "index.html");
const cssPath = path.join(root, "style.css");
const scriptPath = path.join(root, "script.js");

for (const filePath of [htmlPath, cssPath, scriptPath]) {
  assert.ok(fs.existsSync(filePath), `${path.basename(filePath)} should exist`);
}

const html = fs.readFileSync(htmlPath, "utf8");
assert.match(html, /id="todo-form"/, "HTML should include the todo form");
assert.match(html, /id="todo-input"/, "HTML should include the todo input");
assert.match(html, /id="todo-list"/, "HTML should include the todo list");
assert.match(html, /id="clear-completed"/, "HTML should include clear completed action");
assert.match(html, /<script src="\.\/script\.js" defer><\/script>/, "HTML should load script without requiring a dev server");
assert.match(html, /<title>待办清单<\/title>/, "HTML document title should be Chinese");
assert.match(html, /<h1 id="app-title">Todo List<\/h1>/, "HTML app title should be English");
assert.doesNotMatch(html, /<h1 id="app-title">待办清单<\/h1>/, "HTML app title should not show the Chinese heading");

const scriptSource = fs.readFileSync(scriptPath, "utf8");
const { default: vm } = await import("node:vm");
let idCounter = 0;
const sandbox = {
  console,
  crypto: {
    randomUUID: () => `test-id-${(idCounter += 1)}`,
  },
};
sandbox.globalThis = sandbox;
vm.runInNewContext(scriptSource, sandbox, { filename: "script.js" });

const app = sandbox.TodoApp;

let todos = [];
todos = app.addTodo(todos, "  学习 Go  ");
todos = app.addTodo(todos, "写 Todo 页面");

assert.equal(todos.length, 2, "addTodo should append active todos");
assert.equal(todos[0].text, "学习 Go", "addTodo should trim text");
assert.equal(todos[0].completed, false, "new todos should be active");
assert.throws(() => app.addTodo(todos, "   "), /不能为空/, "blank todo should be rejected");

todos = app.toggleTodo(todos, todos[0].id);
assert.equal(todos[0].completed, true, "toggleTodo should flip completion");
assert.equal(app.getRemainingCount(todos), 1, "remaining count should ignore completed todos");
assert.equal(app.filterTodos(todos, "active").length, 1, "active filter should hide completed todos");
assert.equal(app.filterTodos(todos, "completed").length, 1, "completed filter should hide active todos");

todos = app.clearCompleted(todos);
assert.equal(todos.length, 1, "clearCompleted should remove completed todos");

todos = app.deleteTodo(todos, todos[0].id);
assert.equal(todos.length, 0, "deleteTodo should remove a todo by id");

console.log("Smoke test passed");
