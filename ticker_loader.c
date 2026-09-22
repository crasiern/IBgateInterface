#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>
#include <time.h>

int retrieveFile(const char** jsonPointer);
static size_t write_cb(char *contents, size_t size, size_t nmemb, void *stream);
int JSONtoCSV(const char* jsonString);
int needsUpdate();

const char* SEC_URL = "https://www.sec.gov/files/company_tickers.json";
static const char filename[] = "../company_tickers.csv";

// reference https://curl.se/libcurl/c/getinmemory.html for writing sec json to string
struct mem_chunk {
    char *memory;
    size_t size;
};

// HEADER FORMAT: [name],[YEAR][MONTH][DAY],[YEAR][MONTH][DAY] // ex. {company_tickers,20260921,19800514}
// to compare dates, turn to string. 0 place is needed for single digits. If 10, 20, 30, may need to times 10, then math can be done

int main()
{
    time_t now = time(NULL);  
    struct tm *current_time = localtime(&now);
    printf("Year: %d\n", current_time->tm_year + 1900); 
    printf("Month: %d\n", current_time->tm_mon + 1); 
    printf("Day: %d\n", current_time->tm_mday);
    // need time converting function 


    // check header of ticker_loader.csv for timestamp
    // if header < 30 days, do not retrieve new file unless forced?

    // handle errors via ints
    // only run if header < 30 days or 
    // maybe should return a char*?

    const char* jsonString = NULL;
    retrieveFile(&jsonString);
    printf("Size: %zu\n", strlen(jsonString));
    // convert json to csv, add header, and delete json file

    return 0;
}

int retrieveFile(const char** jsonPointer)
{
    curl_global_init(CURL_GLOBAL_ALL);
    CURLcode result;

    CURL* handle = curl_easy_init();
    struct mem_chunk jsonChunk;

    jsonChunk.memory = malloc(1); 
    jsonChunk.size = 0;

    curl_easy_setopt(handle, CURLOPT_URL, SEC_URL);
    curl_easy_setopt(handle, CURLOPT_NOPROGRESS, 1L);
    curl_easy_setopt(handle, CURLOPT_USERAGENT, "ticker_loader crasiern@gmail.com");
    curl_easy_setopt(handle, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(handle, CURLOPT_WRITEDATA, (void *)&jsonChunk);
    curl_easy_perform(handle);

    *jsonPointer = jsonChunk.memory;

    curl_easy_cleanup(handle);
    curl_global_cleanup();
    return (int) result;
}

// borrowed from https://curl.se/libcurl/c/url2file.html
// writes curl output into file
static size_t write_cb(char *contents, size_t size, size_t nmemb, void *stream)
{
    size_t realsize = size * nmemb;
    struct mem_chunk *mem = (struct mem_chunk *)stream;
    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if(!ptr) {
    // change to error that halts program
        printf("not enough memory (realloc returned NULL)\n");
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

// do not run until for loop finished
int JSONtoCSV(const char* jsonString)
{
    // may not need const
    const cJSON *company_index = NULL;
    int status = 0;
    
    cJSON* tickers_json = cJSON_Parse(jsonString);
    if (tickers_json == NULL)
        return 404;
    
    FILE *csvFile = fopen(filesname, "wb");
    // create header

    int index = 0;
    for (;;)
    {
        // hopefully 8 is enough, needs \0
        char indexOfJSON[8];
        const cJSON *company_data = NULL;
        snprintf(indexOfJSON, sizeof(indexOfJSON), "%i", index);
        company_index = cJSON_GetObjectItemCaseSensitive(tickers_json, indexOfJSON);

        // check if null or invalid and break

        cJSON_ArrayForEach(company_data, company_index)
        {
            cJSON *cik_str = cJSON_GetObjectItemCaseSensitive(company_data, "cik_str");
            cJSON *ticker = cJSON_GetObjectItemCaseSensitive(company_data, "ticker");
            cJSON *title = cJSON_GetObjectItemCaseSensitive(company_data, "title");

            // add to new line of csv
        }
        index++;
    }

    cJSON_Delete(tickers_json);
    fclose(csvFile);
}

// should probably take in date
int needsUpdate()
{
    FILE *tickerFile = fopen(filename, "r");
    if (tickerFile == NULL)
    {
        fclose(tickerFile);
        return 1;
    }
    
    char headerLine[256];
    fgets(headerLine, sizeof(headerLine), tickerFile);

    // use strtok() to get each , piece
    // convert to math
    // return 1 if needs update

    fclose(tickerFile);
    return 0;
}
