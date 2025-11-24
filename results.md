# Results

## 1. Summary of Work Performed

As part of this assignment, I implemented a client workflow that
interacts with the Neurolabs Image Recognition API. The workflow
included:

1.  Retrieving available task UUIDs using `/image-recognition/tasks`
2.  Preparing and cleaning image URLs for submission
3.  Submitting URLs in controlled batches to avoid rate limiting
4.  Polling for result UUIDs returned by the API
5.  Fetching each result individually using `/results/{result_uuid}`
6.  Storing all outputs as JSON files for further analysis

All four images submitted were processed successfully.

------------------------------------------------------------------------

## 2. Limitations

The work was constrained primarily by API behaviour, request handling,
and testing limitations rather than model or dataset performance.

### API Limitations

-   **429 Too Many Requests Errors**\
    Submitting too many URLs at once triggered rate limiting.\
    To avoid this, batching was restricted to size **2**, with **3 retry
    attempts** and a **15-second delay** between retries.

-  " **Duplicate Result UUIDs**\
    Two of the submitted images produced **duplicate result UUIDs**,
    meaning multiple results were generated for the same input URL.\
    The pipeline had to handle this by detecting duplicates and
    processing all associated results.\
    This added extra polling calls and additional JSON output files." dont think this was true 

-   **Per-result retrieval requirement**\
    `/results/{result_uuid}` must be called for each UUID individually.\
    No batch results endpoint exists, increasing API load and
    contributing to rate-limit sensitivity.

-   **Processing time variability**\
    Inference completion time was inconsistent, requiring polling with
    fixed delays.

### Implementation Limitations

-   **Simplified Exponential Backoff**\
    While exponential backoff was implemented, simplified values were
    used:

    -   Batch size: **2**
    -   Retries: **3**
    -   Delay: **15 seconds**

    These constants were chosen to avoid long waits during testing but
    do not represent a full exponential strategy.

-   **URL Formatting Issues**\
    Several URLs contained angle brackets (`< >`) or extra characters.\
    Submissions only succeeded after cleaning the URLs.

### Testing Constraints (Given as Part of the Assignment)

-   The four images submitted were identical.
-   Dataset had fixed lighting, angle, and product arrangement.
-   These constraints limited the ability to test API behaviour under
    diverse conditions.

------------------------------------------------------------------------

## 3. Assumptions

### API Behaviour Assumptions

-   Task UUIDs remain valid throughout the session.
-   API endpoints return consistent response schemas as documented.
-   A status of `"PROCESSED"` indicates a complete and valid result.

### Request Handling Assumptions

-   Submitting URLs in small batches (size 2) is the optimal strategy to
    avoid rate limiting.
-   A retry count of 3, combined with 15-second delays, is sufficient to
    recover from temporary rate-limit events.
-   If the API accepts a cleaned URL, it is considered valid input.

### Data Handling Assumptions

-   JSON responses can be stored locally without modification.
-   Missing fields in the response (e.g., missing modalities) are
    expected and do not represent API failure.

------------------------------------------------------------------------

## 4. Conclusion

The API workflow was successfully executed end-to-end, with results
reliably returned after implementing controlled batching and a simple
backoff strategy.\
Most limitations encountered were related to API request constraints
(429 errors), duplicate result UUIDs, and the testing configuration
provided in the task.

The pipeline demonstrates a working, robust interaction with the
Neurolabs Image Recognition API, including error handling, retries, and
structured result storage.
