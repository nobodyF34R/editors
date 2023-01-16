﻿#pragma execution_character_set("utf-8")

#ifndef EQUIPMENTTAB_H
#define EQUIPMENTTAB_H

#include <QWidget>
#include <QtCore>
#include <QCheckBox>

#include "listtab.h"
#include "gameconfig.h"
#include "gamedata.h"

#include "ui_equipmenttabform.h"

class EquipmentTab : public ListTab, private Ui::EquipmentTabForm
{
    Q_OBJECT

public:
    explicit EquipmentTab(SaveManager *mgr, QWidget *parent=0, int sectionId=-1);
    ~EquipmentTab();
public slots:
    void update();
    void loadItemAt(int row);
    void writeItemAt(int row);
    void loadCurrentItem();
    void writeCurrentItem();

private:
    Ui::EquipmentTabForm *form;
};

#endif // EQUIPMENTTAB_H
