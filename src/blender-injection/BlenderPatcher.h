#pragma once

#include "BlenderObj.h"
#include "BlenderPatch.h"

#pragma comment(lib, "version.lib")

extern "C" void DropEventHook(const char*, char*);

extern "C" bool View3DImaEmptyDropPollHook(void* c, void* drag, void* event);


class BlenderPatcher
{
private:
    std::string _version;
    std::string _pattern;
    std::unordered_map<std::uintptr_t, std::vector<unsigned char>> _originals;

    inline static BlenderPatcher* _instance = nullptr;

    BlenderPatcher()
    {
        this->_version = "0.0.0";
    }

    void FetchVersion();
    [[nodiscard]] BlenderPatch GetPatch() const;
    void ApplyInjector();
    void RestoreInjector();
    void GetAssemblyCodeFrom(const Injector::memory_pointer_tr& at, void* ret, unsigned int bytes) const;
    void ReplaceInstructionWithCall(const Injector::memory_pointer_tr& at, void* dest, bool ret = false) const;
    void ReplaceFunctionWithCall(const Injector::memory_pointer_tr& at, void* dest, unsigned int paddings = 0) const;

public:
    static BlenderPatcher* GetInstance();

    void Patch();
    void UnPatch();

    bool View3DImaDropPoll(Context* c, wmDrag* drag, wmEvent* event) const;
    void* EDView3dGiveObjectUnderCursor(Context* c, int mvals[2]) const;
    void RunStringEval(void* c, const char* imports[], const char* expression) const;
};

bool LaunchDebugger();
