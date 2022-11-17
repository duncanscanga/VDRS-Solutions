# Duncan:

Dev Branch: DS_67_TestSqlInjectionListingCreate

Progress: Have read the file line by line and all payloads result in a listing not being created. All tests pass.

Difficulties: Some difficulty with pip with the PyYAML and seleniumbase installation but have been resolved.

Plan: Going to improve requirement checking that takes place in the actual create_listing function. Currently, I check the length of the value and then confirm whatever is being passed is actually an integer. I will add a check for the bounds of the values.

# Rahul:

Dev Branch: 69-SQL-Injection-Register

Progress: All the tests pass for the SQL injection using the name
and email as parameters

Difficulties: Syntax errors and figuring out how to use the 
line parameter to replace the name and email.
Also had difficulty installing docker.

Plan: Go to the office hours to figure out how to use
the parameters and the SQL injection text file correctly.

# Vasuki:

Dev Branch: vasuki-a5

Progress: Created tests to ensure injection inputs are rejected. 

Difficulties: Figuring out how to block the malicious listing description inputs. 

Plan: Get feedback from the teammates on the PR. Make changes as necessary. 

# Sam:

Dev Branch: sam-register-injection, sam-a5
Progress: Implemented Docker, started working on the Register() injection testing
Difficulties: Trouble with implementing checks for some injections since many of them are valid passwords
Plan: Find the most efficient check to ensure the inputs are not passed in
