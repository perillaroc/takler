from takler.tasks import ShellScriptTask


def test_create():
    task = ShellScriptTask(
        name="initial",
        script_path="/home/johndoe/takler/script/initial.takler"
    )
    assert task.name == "initial"
    assert task.script_path == "/home/johndoe/takler/script/initial.takler"



