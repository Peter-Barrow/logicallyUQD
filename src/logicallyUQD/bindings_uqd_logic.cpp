#include "bindings_uqd_logic.h"
#include "CLogic.h"
#include "CTimeTag.h"
#include <cstdio>
#include <cstring>
#include <stdexcept>
#include <stdint.h>
#include <vector>

extern "C" {

CTimeTag_ptr
CTimeTag_create() {
    return new TimeTag::CTimeTag();
}

void
CTimeTag_destroy(CTimeTag_ptr timetag) {
    delete reinterpret_cast<TimeTag::CTimeTag*>(timetag);
}

void
CTimeTag_open(CTimeTag_ptr timetag, int nr) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->Open(nr);
}

int
CTimeTag_isOpen(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    return ptr->IsOpen() ? 1 : 0;
}

void
CTimeTag_close(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->Close();
}

void
CTimeTag_calibrate(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->Calibrate();
}

void
CTimeTag_setInputThreshold(CTimeTag_ptr timetag, int input, double voltage) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetInputThreshold(input, voltage);
}

void
CTimeTag_setFilterMinCount(CTimeTag_ptr timetag, int MinCount) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetFilterMinCount(MinCount);
}

void
CTimeTag_setFilterMaxTime(CTimeTag_ptr timetag, int MaxTime) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetFilterMaxTime(MaxTime);
}

double
CTimeTag_getResolution(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    return ptr->GetResolution();
}

int
CTimeTag_getFpgaVersion(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    return ptr->GetFpgaVersion();
}

void
CTimeTag_setLedBrightness(CTimeTag_ptr timetag, int percent) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetLedBrightness(percent);
}

// const char* CTimeTag_getErrorText(CTimeTag_ptr timetag, int flags) {
//     auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
//     return ptr->GetErrorText(flags).c_str();
// }

void
CTimeTag_enableGating(CTimeTag_ptr timetag, int enable) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->EnableGating(enable != 0);
}

void
CTimeTag_gatingLevelMode(CTimeTag_ptr timetag, int enable) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->GatingLevelMode(enable != 0);
}

void
CTimeTag_setGateWidth(CTimeTag_ptr timetag, int duration) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetGateWidth(duration);
}

void
CTimeTag_switchSoftwareGate(CTimeTag_ptr timetag, int onOff) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SwitchSoftwareGate(onOff != 0);
}

void
CTimeTag_setInversionMask(CTimeTag_ptr timetag, int mask) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetInversionMask(mask);
}

void
CTimeTag_setDelay(CTimeTag_ptr timetag, int Input, int Delay) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetDelay(Input, Delay);
}

int
CTimeTag_readErrorFlags(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    return ptr->ReadErrorFlags();
}

int
CTimeTag_getNoInputs(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    return ptr->GetNoInputs();
}

void
CTimeTag_useTimetagGate(CTimeTag_ptr timetag, int use) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->UseTimetagGate(use != 0);
}

void
CTimeTag_useLevelGate(CTimeTag_ptr timetag, int use) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->UseLevelGate(use != 0);
}

int
CTimeTag_levelGateActive(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    return ptr->LevelGateActive() ? 1 : 0;
}

void
CTimeTag_use10MHz(CTimeTag_ptr timetag, int use) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->Use10MHz(use != 0);
}

void
CTimeTag_setFilterException(CTimeTag_ptr timetag, int exception) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->SetFilterException(exception);
}

void
CTimeTag_startTimetags(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->StartTimetags();
}

void
CTimeTag_stopTimetags(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    ptr->StopTimetags();
}

int
CTimeTag_readTags(CTimeTag_ptr timetag,
                  c_ChannelType** channel_ret,
                  c_TimeType** time_ret) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    int count = ptr->ReadTags(*channel_ret, *time_ret);

    // printf("Count:\t%d\n", count);

    // int i = 0;
    // for (i = 0; i < count; i++) {
    //     printf("ch[%d]\t%llu\n", channel_ret[i], (uint64_t)time_ret[i]);
    // }
    return count;
}

void
CTimeTag_printTags(CTimeTag_ptr timetag,
                   c_ChannelType* channels,
                   c_TimeType* timestamps) {

    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    int count = ptr->ReadTags(channels, timestamps);
    printf("Count:\t%d\n", count);

    int i = 0;
    for (i = 0; i < count; i++) {
        printf("ch[%d]\t%llu\n", channels[i], (uint64_t)timestamps[i]);
    }
}

CLogic_ptr
CLogic_create(CTimeTag_ptr timetag) {
    auto ptr = reinterpret_cast<TimeTag::CTimeTag*>(timetag);
    // return new TimeTag::CLogic(ptr)
    return ptr->GetLogic();
}

void
CLogic_switchLogicMode(CLogic_ptr logic) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SwitchLogicMode();
}

void
CLogic_setWindowWidth(CLogic_ptr logic, int window) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SetWindowWidth(window);
}

void
CLogic_setWindowWidthEx(CLogic_ptr logic, int index, int window) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SetWindowWidthEx(index, window);
}

void
CLogic_setDelay(CLogic_ptr logic, int input, int delay) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SetDelay(input, delay);
}

long long
CLogic_readLogic(CLogic_ptr logic) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    return ptr->ReadLogic();
}

int
CLogic_calcCountPos(CLogic_ptr logic, int pattern) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    return ptr->CalcCountPos(pattern);
}

int
CLogic_calcCount(CLogic_ptr logic, int pos, int neg) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    return ptr->CalcCount(pos, neg);
}

long long
CLogic_getTimeCounter(CLogic_ptr logic) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    return ptr->GetTimeCounter();
}

void
CLogic_setOutputWidth(CLogic_ptr logic, int width) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SetOutputWidth(width);
}

void
CLogic_setOutputPattern(CLogic_ptr logic, int output, int pos, int neg) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SetOutputPattern(output, pos, neg);
}

void
CLogic_setOutputEventCount(CLogic_ptr logic, int events) {
    auto ptr = reinterpret_cast<TimeTag::CLogic*>(logic);
    ptr->SetOutputEventCount(events);
}

} // extern "C"
