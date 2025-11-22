# Results

## 1. Summary of Work Performed

As part of this assignment, I implemented a client workflow that
interacts with the Neurolabs Image Recognition API. The workflow
included:

-   Retrieving available task UUIDs using `/image-recognition/tasks`
-   Loading image URLs from ambient.csv (8 URLs) and cooler.csv (2 URLs)
-   Cleaning and validating URLs before submission
-   Submitting URLs in controlled batches to avoid rate limiting
-   Polling for result UUIDs returned by the API
-   Fetching each result individually using `/results/{result_uuid}`
-   Storing all outputs as JSON files for further analysis

All ten images were successfully processed.

## 2. Limitations

The work was constrained primarily by API behaviour, request handling,
and dataset constraints rather than model performance.

### API Limitations

#### 429 Too Many Requests Errors

Submitting too many URLs or polling too frequently triggered rate
limiting.

To mitigate this: - Batch size was restricted to 2 URLs - A 15-second
delay was enforced after each batch - Retries used exponential backoff
(`2**attempt`) - Maximum retries per request: 3

This stabilised submissions and prevented repeated 429 responses.

#### Per-result retrieval requirement

`/results/{result_uuid}` must be queried one at a time.\
Since no batch results endpoint exists, this significantly increases API
load and contributes to rate-limit sensitivity.

#### Processing time variability

Inference completion time varied from image to image, requiring repeated
polling with fixed delays to ensure results were ready.

### Implementation Limitations

#### Simplified Exponential Backoff

While exponential backoff was implemented, it was simplified for speed
during testing:

-   Batch size: 2
-   Retries: 3
-   Fixed 15-second wait between batches
-   Exponential backoff only applied on retries

A production system would require: - Dynamic jitter - Longer maximum
waiting periods - More aggressive scaling of delays

#### URL Formatting Issues

Some URLs contained invalid characters such as `< >` or stray
whitespace.\
These caused API submission failures until cleaned.

This required a preprocessing step to normalise and validate all URLs.

### Testing Constraints

These constraints came from the dataset provided: - Image URLs were
fixed and sourced directly from ambient.csv and cooler.csv - A total of
10 URLs were available (8 ambient, 2 cooler) - No variation existed in
lighting, angle, perspective, or product arrangement

Because of this, the evaluation focused on API workflow behaviour rather
than model robustness across diverse scenarios.

## 3. Assumptions

### API Behaviour Assumptions

-   Task UUIDs remain valid throughout the session
-   API responses follow the documented schema
-   A "PROCESSED" status indicates a complete and usable result

### Request Handling Assumptions

-   Small batches (size 2) help prevent rate-limiting errors
-   3 retries with exponential backoff and 15-second batch delays allow
    recovery from temporary 429 responses
-   A cleaned URL accepted by the API is considered a valid input image

### Data Handling Assumptions

-   JSON responses can be stored directly without additional validation
-   Missing modality fields or score values are expected and do not
    indicate a failure

## 4. Conclusion

The API workflow was successfully executed end-to-end, with results
reliably returned after implementing controlled batching, URL cleaning,
and a simple retry strategy.

The most significant challenges involved: - Rate limiting (429 errors) -
URL formatting issues - The limited variety of the provided dataset

Despite these constraints, the pipeline demonstrated a robust
interaction with the Neurolabs Image Recognition API --- including error
handling, retries, result retrieval, and structured JSON output suitable
for downstream analysis.
