#include "itemtab.h"

ItemTab::ItemTab(SaveManager* mgr, QWidget* parent, int sectionId)
    : ListTab(mgr, parent, sectionId)
    , form(new Ui::ItemTabForm)
{
    QWidget* w = new QWidget(this);
    form->setupUi(w);
    ui->form->addWidget(w);

    this->setNum1Offset(0x0);
    this->setItemSize(0x0C);

    for (int i = 0; i < this->getItemsCount(); ++i) {
        ui->listWidget->addItem(QString(""));
    }

    /* intert items into combobox */
    foreach (const dataentry_t& it, GameData::getInstance().getData("element")) {
        form->itemCB->addItem(it.second.value("name"), it.first);
    }
    foreach (const dataentry_t& it, GameData::getInstance().getData("consume")) {
        form->itemCB->addItem(it.second.value("name"), it.first);
    }
    form->itemCB->setCurrentIndex(-1);
    connect(ui->listWidget, SIGNAL(currentRowChanged(int)), SLOT(loadItemAt(int)));
    connect(ui->resetButton, SIGNAL(clicked(bool)), SLOT(loadCurrentItem()));
    connect(ui->applyButton, SIGNAL(clicked(bool)), SLOT(writeCurrentItem()));
}

ItemTab::~ItemTab()
{
    delete form;
}

void ItemTab::setLocale(SaveManager::GameLocale)
{
}

void ItemTab::updateList()
{
    for (int i = 0; i < this->getItemsCount(); ++i) {
        quint32 ItemId = this->read<quint32>(0x04 + 0x0C * i);
        int itemIndex = form->itemCB->findData(ItemId);
        if (itemIndex >= 0) {
            ui->listWidget->item(i)->setText(
                form->itemCB->itemText(itemIndex));
        } else {
            ui->listWidget->item(i)->setText(tr("(不明)"));
        }
    }
    this->setButtonsEnabled(true);
    ui->listWidget->setCurrentRow(0);
    this->loadCurrentItem();
}

void ItemTab::loadItemAt(int row)
{
    if (row >= 0 && row < this->getItemsCount()) {
        /* 0x10 is for header */
        quint16 num1 = this->read<quint16>(0x00 + 0x0C * row);
        quint16 num2 = this->read<quint16>(0x02 + 0x0C * row);
        quint32 ItemId = this->read<quint32>(0x04 + 0x0C * row);
        quint8 itemCount = this->read<quint8>(0x08 + 0x0C * row);
        form->num1SB->setValue(num1);
        form->num2SB->setValue(num2);
        form->countSB->setValue(itemCount);

        /* load item */
        form->itemCB->setCurrentIndex(form->itemCB->findData(ItemId));
    }
}

void ItemTab::writeItemAt(int row)
{
    if (row >= 0 && row < this->getItemsCount()) {
        this->write<quint16>(form->num1SB->value(), 0x00 + 0x0C * row); // num1
        this->write<quint16>(form->num2SB->value(), 0x02 + 0x0C * row); // num2
        if (form->itemCB->currentIndex() >= 0) {
            this->write<quint32>(
                form->itemCB->currentData().value<quint32>(),
                0x04 + 0x0C * row); // ItemId
        }
        this->write<quint8>(form->countSB->value(), 0x08 + 0x0C * row); // itemCount
    }

    /* update */
    this->loadItemAt(row);
    quint32 ItemId = form->itemCB->currentData().value<quint32>();
    int itemIndex = form->itemCB->findData(ItemId);
    if (itemIndex >= 0) {
        ui->listWidget->item(row)->setText(
            form->itemCB->itemText(itemIndex));
    } else {
        ui->listWidget->item(row)->setText(tr("(不明)"));
    }
}

void ItemTab::loadCurrentItem()
{
    int i;
    if ((i = ui->listWidget->currentRow()) >= 0) {
        this->loadItemAt(i);
    }
}

void ItemTab::writeCurrentItem()
{
    int i;
    if ((i = ui->listWidget->currentRow()) >= 0) {
        this->writeItemAt(i);
    }
}