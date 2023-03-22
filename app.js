const { PythonShell } = require("python-shell");

const TRIGGER_WORD = "TwojeImie";

const options = {
  mode: "text",
  pythonOptions: ["-u"],
  scriptPath: "./",
};

const pyShell = new PythonShell("a1.py", options);

pyShell.on("message", (message) => {
  if (message.toLowerCase().includes(TRIGGER_WORD.toLowerCase())) {
    console.log(`Słowo wyzwalające wykryte: ${message}`);
  }
});

pyShell.end((err, code, signal) => {
  if (err) throw err;
  console.log(`Zakończono z kodem ${code} i sygnałem ${signal}`);
});
