Title: Create a Simple AI Assistant Using LLama 3: A Proof of Concept
Date: 2024-07-02
Tags: Python,Machine Learning, LLM, Large Language Model, LLama 3, Nima Moradi
Category: Guide
Summary: Create a simple AI assistant using LLama 3 proof of concept

In this guide, we'll explore how to create a simple AI assistant using LLama 3, a state-of-the-art Large Language Model. With the growing popularity of AI-powered tools like GitHub Copilot and Amazon Q&A, building your own AI assistant may seem daunting at first. However, with the help of LLama 3 and the Python interface, we'll demonstrate how to create a quick and functional demo.

The Code

Here's the code we used in our demonstration:

<pre>
<code>
def give_recommendations(lang, code, line):
    mes = f"""
    you are a tool like github copilot, I have a code file and I need your help to provide recommendations for a specific line. Below is the relevant code snippet and given this code 
**File Type:** {lang}

**Code Snippet:**

`{lang}
{code}
`
i want recomendations for filling code after this `{line}` part, avoid unnecessary comments
    """
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": mes
            },
        ],
    )
    answer = response["message"]["content"]
    return extract_code_blocks(lang, answer)
</code>
</pre>

Feel free to explore and modify it to suit your needs!

### Sample Test Cases

We've included two sample test cases for you to try out:
<pre>
<code>
    lang_1 = 'python'

    code_test_1 = """
    def calculate_area(radius):
    # This function calculates the area of a circle.
    import math
    area = 
    return area
    """

    section_1 = ' area = '

    print(give_recommendations(lang_1, code_test_1, section_1))

    lang_2 = 'java'
    code_test_2 = """
static void bubbleSort(int arr[], int n)
    {
        int i, j, temp;
        boolean swapped;
        for (i = 0; i < n - 1; i++) {
            swapped = false;
            for (j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    
                    // Swap arr[j] and arr[j+1]
                   
                }
            }

            // If no two elements were
            // swapped by inner loop, then break
            if (swapped == false)
                break;
        }
    }
    """

    section_2 = """// Swap arr[j] and arr[j+1]
                   """
    print(give_recommendations(lang_2, code_test_2, section_2))
</code>
</pre>
These test cases will give you a sense of how the AI assistant can be used in everyday scenarios.

### Recommendations and Code Snippets

Here are some code snippets and recommendations we came up with during our experimentation with LLama 3
```python
[
    ('python', 'import math\n\ndef calculate_area(radius):\n    area = math.pi * (radius ** 2)\n    return area')
    ('python', 'import math\n\ndef calculate_area(radius):\n    area = math.pi * (radius ** 2)\n    return area'),
    ('python', 'import math\n\ndef calculate_area(radius):\n    pi = 22 / 7\n    area = pi * (radius ** 2)\n    return area'), ('python', 'import math\n\ndef calculate_area(radius):\n    try:\n        area = math.pi * (radius ** 2)\n        return area\n    except TypeError:\n        return "Error: Radius must be a number"')
]
[
    ('java', 'temp = arr[j];\narr[j] = arr[j + 1];\narr[j + 1] = temp;'),
    ('java', 'int[] tempArr = new int[1];\ntempArr[0] = arr[j + 1];\nArrays.swap(arr, j, j + 1);\narr[j + 1] = tempArr[0];'),
    ('java', 'int temp = arr[j + 1];\narr[j + 1] = arr[j];\narr[j] = temp;')
]

```

These code snippets showcase some interesting ideas and approaches you can take when building your own AI assistant.
### Prompts from GitHub
Here are some prompts we found in the GitHub repository for ChatGPT, which can be used as inspiration for our LLama 3-powered AI assistant:
<pre>
<code>
  public static final Prompt IMPLEMENT = new Prompt("Act like a professional programmer. From concise requests you infer the intended functionality. First write out the idea in plain text, as a comment in the appropirate programming language. Then write out the code in a function, multiple functions or the appropriate data format (such as xml, json or any other). Now, implement the following specification using code in the mentioned language. ");
    public static final Prompt CHAT = new Prompt("You are a professional assistant. You are chatting with the programmer about the following topic: ");
    public static final Prompt FIX = new Prompt("analyze and fix the following error");
    public static final Prompt DOCUMENTATION = new Prompt("write documentation for the following code");
    public static final Prompt EXPLAIN = new Prompt("explain and summarize the following");
    public static final Prompt COMPLETE = new Prompt("complete the following code");
    public static final Prompt CONVERT = new Prompt("convert the following code by transpiling it to ");
    public static final Prompt REVIEW = new Prompt("analyze, code review and make suggestions to improve the following code");
    public static final Prompt TESTS = new Prompt("emit tests for the following code");
    public static final Prompt OPTIMIZE = new Prompt("analyze the code for optimization potential, then optimize the code accordingly");
    public static final Prompt IMPROVE = new Prompt("analyze, code review the following code, then improve and optimize the code accordingly");
    public static final Prompt EDIT = new Prompt("edit the following code using the following instructions: ");
    public static final Prompt EDIT_CODE_WITH_COMMAND = new Prompt("edit the following code: %s\n" +
            "using the following instructions: %s");
    public static final Prompt EXECUTE = new Prompt("Given english instructions, find the right terminal command in a zsh shell. The command should be in the following format: ```bash <command>```");

</code>
</pre>
That's it for now! If you're interested in exploring more, feel free to leave a comment or ask us a question in medium. Happy coding!