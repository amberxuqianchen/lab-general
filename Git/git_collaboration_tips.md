# How to Contribute to An Existing Repository: A Step-by-Step Guide for Social Scientists

## Step 1: Familiarize yourself with the project
- Read the project's documentation (README.md) to understand its purpose and overall functionality.
- Learn about the Python scripts used in the project and their respective roles.

## Step 2: Set up the development environment
- Install Python (version 3.8 or higher).
- Install required Python packages and libraries (e.g., pandas, gensim, matplotlib, numpy).
- Clone or download the project from the GitHub repository.

## Step 3: Understand the main scripts and files
- Study the Python scripts and explore their code.
- Investigate the main.py script, which is responsible for executing all functions in corresponding files to understand their purpose.

## Step 4: Explore and analyze the data
- Run the main.py script and analyze the output.
- Adjust the target words, foundational words, and word2vec models as necessary.
- Re-run the main.py script to update the results based on your specific requirements.

## Step 5: Propose and implement improvements
- Identify areas where improvements can be made, such as different analysis paths.
- Develop and implement new features or improvements to the scripts.
- Be cautious of editing files in data folder.

## Step 6: Document your work
- Write clear and concise documentation on your work and any changes made.
- Update the README.md file if necessary to reflect the project's current state.

## Step 7: Share your work and collaborate with others

### 7.1 Create your own branch
- Before making any changes, make sure you create your own branch to keep your work separate from the main branch:
  ```
  git checkout -b my-feature-branch
  ```

### 7.2 Implement and commit your changes
- Implement your changes and improvements to the project.
- Add and commit the changes to your local branch:
  ```
  git add file1.py file2.py ...
  git commit -m "A descriptive message about your changes"
  ```

### 7.3 Keep your branch up-to-date with the main branch
- Regularly pull the latest changes from the main branch to ensure your work is based on the most recent version:
  ```
  git checkout main
  git pull origin main
  git checkout my-feature-branch
  git merge main
  ```

### 7.4 Push your local branch to the remote repository
- After implementing and testing your changes locally, push your branch to the remote repository:
  ```
  git push origin my-feature-branch
  ```

### 7.5 Create a pull request
- On the GitHub project page, navigate to the "Pull requests" tab and create a new pull request.
- Select your remote branch (my-feature-branch) as the source, and the main remote branch as the destination.
- Provide a clear and informative title and description for your pull request.
- Request code review from your peers or supervisors to gather feedback on your work.

### 7.6 Review and address feedback
- Address any feedback provided by your peers during the code review.
- Make the necessary changes and push them to your branch.
- Update the pull request with a comment explaining the modifications.

### 7.7 Merge your pull request
- Once your changes have been reviewed and approved, one of the project maintainers will merge your pull request into the main branch.
- After the merge, remember to delete your local and remote feature branch, as it is no longer needed:
  ```
  git branch -d my-feature-branch
  git push origin --delete my-feature-branch
  ```

- **Use issues:** Use issues to track bugs, feature requests, and other tasks, and to assign tasks to specific people.