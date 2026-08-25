import requests

leetcode_url = "https://leetcode.com/graphql"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": "https://leetcode.com/",
    "Origin": "https://leetcode.com",
}

def get_all_questions():
    all_questions = []

    limit = 50
    skip = 0

    query = """
    query problemsetQuestionList(
        $categorySlug: String,
        $limit: Int,
        $skip: Int,
        $filters: QuestionListFilterInput
    ) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            totalNum
            data {
                questionFrontendId
                title
                titleSlug
                difficulty
                topicTags {
                    name
                    slug
                }
                content
            }
        }
    }
    """

    while True:
        variables = {
            "categorySlug": "",
            "skip": skip,
            "limit": limit,
            "filters": {}
        }   

        response = requests.post(
            leetcode_url,
            headers=headers,
            json={
                "query": query,
                "variables": variables,
                "operationName": "problemsetQuestionList",
            },
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        question_data = result["data"]["problemsetQuestionList"]

        total_num = question_data["totalNum"]
        print(total_num)

        questions = question_data["data"]

        all_questions.extend(questions)

        skip += limit
        if skip >= total_num:
            break

        return all_questions

def get_solution():
    query = """
        query problemsetQuestionList(
        $categorySlug: String,
        $limit: Int,
        $skip: Int,
        $filters: QuestionListFilterInput
    ) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters 
        ) {
            total: totalNum
            questions: data {
                frontendQuestionId: questionFrontendId
                title
                titleSlug
                difficulty
                paidOnly: isPaidOnly
                hasSolution
                hasVideoSolution
            }
        }
    }
    """

    while True:
        variables = {
            "categorySlug": "",
            "skip": 0,
            "limit": 1,
            "filters": {
                "searchKeywords": "28"
            }
        }   

        response = requests.post(
            leetcode_url,
            headers=headers,
            json={
                "query": query,
                "variables": variables,
                "operationName": "problemsetQuestionList",
            },
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        return result["data"]["problemsetQuestionList"]["questions"][0]["titleSlug"]

def get_question_details(title_slug):
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            content
            isPaidOnly
            difficulty

            similarQuestions

            topicTags {
                name
                slug
            }

            codeSnippets {
                lang
                langSlug
                code
            }

            hints

            solution {
                id
                canSeeDetail
            }

            exampleTestcases
            metaData
        }
    }
    """

    variables = {
        "titleSlug": title_slug
    }

    response = requests.post(
        leetcode_url,
        headers=headers,
        json={
            "query": query,
            "variables": variables,
            "operationName": "questionData",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def main():
    #data = getAllQuestions()
    solution_data = get_solution()
    print(solution_data)
    solution = get_question_details(solution_data)
    print(solution)
    #print(data)


if __name__ == "__main__":
    main()
